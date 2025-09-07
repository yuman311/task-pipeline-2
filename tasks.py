import requests
import streamlit as st
from concurrent.futures import ThreadPoolExecutor, as_completed
import cohere

# <---------------- Streamlit Inputs ---------------->
st.title("Dynamic Task Pipeline")
max_id = 194
x = st.number_input("Enter value for x", value=2, min_value=1, max_value=max_id)
y = st.number_input("Enter value for y", value=3, min_value=1, max_value=max_id // max(1, x))

operation = st.selectbox(
    "Choose operation", 
    ["multiply", "add"], 
    index=0 
)
st.write(f"Selected operation: {operation}")

# <---------------- Task Pipeline Class ---------------->
class TaskPipeline:
    def __init__(self, cohere_api_key, execution_mode="sequential"):
        self.context = {}
        self.execution_mode = execution_mode
        self.tasks = []
        self.co = cohere.ClientV2(cohere_api_key)
        self.PYTHON_FUNCTIONS = {"multiply": self.multiply, "add": self.add}
        self.TASK_EXECUTORS = {
            "python": self.run_python_task,
            "api": self.run_api_task,
            "llm": self.run_llm_task,
        }

    # <---------------- Python Functions ---------------->
    @staticmethod
    def multiply(x, y):
        return x * y

    @staticmethod
    def add(x, y):
        return x + y

    # <---------------- Task Runners ---------------->
    def run_python_task(self, task):
     
        inputs = task['inputs']
        return self.PYTHON_FUNCTIONS[task["function"]](**inputs)

    def run_api_task(self, task):
        url = task["endpoint"]
        input_id = self.context.get(task["inputs"])
        if input_id is not None:
            try:
                input_id = int(input_id)
            except:  # noqa: E722
                input_id = 0
        if input_id:
            url = f"{url}/{input_id}"
        resp = requests.request(task.get("method", "GET").upper(), url)
        resp.raise_for_status()
        data = resp.json()
        return data if input_id else data.get("products", [data])[0]

    def run_llm_task(self, task):
        prompt = f"Write a poem about {self.context[task['inputs']]['title']}"
        try:
            resp = self.co.chat(
                model="command-a-03-2025",
                messages=[{"role": "user", "content": prompt}],
            )
            return resp.message.content[0].text
        except Exception as e:
            return f"LLM task failed: {str(e)}"

    # <---------------- Pipeline Execution ---------------->
    def execute_task(self, task, update_callback):
        try:
            output = self.TASK_EXECUTORS[task["type"]](task)
            self.context[task["id"]] = output
            update_callback(task["id"], "completed", output)
            return output
        except Exception as e:
            update_callback(task["id"], "failed", str(e))
            raise

    def run_pipeline(self, tasks, update_callback):
        self.tasks = tasks
        if self.execution_mode == "sequential":
            for task in self.tasks:
                self.execute_task(task, update_callback)
        elif self.execution_mode == "parallel":
            with ThreadPoolExecutor() as executor:
                futures = {executor.submit(self.execute_task, t, update_callback): t for t in self.tasks}
                for f in as_completed(futures):
                    f.result()
        update_callback("pipeline", "done", self.context)
        return self.context

# <---------------- Streamlit Callback ---------------->
def st_update(task_id, status, output):
    st.write(f"**Task {task_id} - {status}:** {output}")

# <---------------- Run Pipeline on Button Click ---------------->
if st.button("Run Pipeline"):
    sample_pipeline = [
        {"id": "task1", "type": "python", "function": operation, "inputs": {"x": x, "y": y}},
        {"id": "task2", "type": "api", "endpoint": "https://dummyjson.com/products", "method": "GET", "inputs": "task1"},
        {"id": "task3", "type": "llm", "inputs": "task2"}
    ]
    
    pipeline = TaskPipeline(cohere_api_key="3LAIk2VFpjysFv60RmAVJmMKjXECam9zy6qRaq7s")
    pipeline.run_pipeline(sample_pipeline, st_update)
