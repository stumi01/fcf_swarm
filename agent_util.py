import json
from typing import Sequence, Any, Dict

from langchain.agents import create_react_agent, AgentExecutor
from langchain.agents.output_parsers.react_single_input import FINAL_ANSWER_ACTION
from langchain_core.exceptions import OutputParserException
from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import BaseTool

task_without_tools = "For this task you dont have to use any tools!\n"

template = """Answer the following questions as best you can. 
You have access to the following tools: {tools}

To use a tool, please use the following format:
```
Question: the input question you must answer
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
```
# (this Thought/Action/Action Input/Observation can repeat N times)

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:
```
Question: the input question you must answer
Thought: Do I need to use a tool? No
Final Answer: [your response here]
```

Begin!
Previous conversation history:

Question: {input}
{agent_scratchpad}"""


def generate_agent_executor(model: BaseLanguageModel, tools: Sequence[BaseTool], ask: str) -> AgentExecutor:
    prompt = PromptTemplate.from_template(template)
    agent = create_react_agent(model, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True,
                         handle_parsing_errors="Check you output and make sure it conforms! Do not output an action and a final answer at the same time. DONT FORGET!! the user's question was: {}".format(
                             ask))


def adjust_for(tools: Sequence[BaseTool], question: str) -> str:
    return task_without_tools + question if not tools else question


def find_final_answer(text: str) -> str:
    print("Handling error: {}".format(text))
    if FINAL_ANSWER_ACTION in text:
        return text.split(FINAL_ANSWER_ACTION)[-1].strip()
    else:
        raise ValueError(text)


def execute_task(model: BaseLanguageModel, tools: Sequence[BaseTool], question: str) -> Dict[str, Any]:
    ask = adjust_for(tools, question)
    agent_executor = generate_agent_executor(model, tools, ask)
    print("######################")
    print("Executing task: {}".format(question))
    try:
        return agent_executor.invoke({"input": ask}, return_only_outputs=True)
    except OutputParserException as e:
        return {"output": find_final_answer(e.message)}
    except ValueError as e:
        return {"output": find_final_answer(e.__str__())}
    except Exception as e:
        raise e
