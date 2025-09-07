# Problem Statement:
Design a configurable pipeline of tasks in Python (preferably configurable in a json structure) that can
execute tasks of three types:
1. Tasks that execute regular python code to produce some output for a given set of inputs
2. Tasks that are defined as external apis (create your own contract preferably some standard
specification)
3. Tasks that are prompt driven which will call LLMs to produce output (use any openly available
LLM api or else mock it based on the specifications from Open AI’s api contract)
 
These tasks can run in sequential or in parallel mode depending on how the pipeline is created.
The output from the precending tasks can be used as an input to the next set of tasks as defined in
the configrations.
Design a high performing python system that can achieve this. Please also capture the requirements
of regular updates being sent to the caller so that at the completion of every step of the pipeline the
caller gets and update and when the whole pipeline is done, caller gets a done signal.



## Features

- **Python Tasks**: Execute functions like `multiply` or `add` with dynamic inputs.
- **API Tasks**: Fetch data from external APIs using task outputs as input.
- **LLM Tasks**: Generate content using Cohere’s API.
- **Dynamic Inputs**: Users can provide `x` and `y` values via Streamlit UI.
- **Operation Selection**: Choose between multiplication or addition.
- **Live Updates**: Pipeline execution updates displayed in real-time.
- **Refresh Button**: Rerun the pipeline anytime with new inputs.

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yuman311/task-pipeline-2.git
cd task-pipeline-2
```
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate 

pip install -r requirements.txt

streamlit run tasks.py
