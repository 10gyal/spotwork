"""
Given a url, the agent scrapes through the website and outputs the content of the webpage containing the job details.
Uses Jina AI to read the content of the webpage.
"""

from typing import Literal

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.graph import MessagesState, END
from langgraph.types import Command
from langchain_core.tools import tool
import requests
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field
from typing import List, Annotated
from langchain_experimental.utilities import PythonREPL


load_dotenv()

# Initialize LLM with correct model name
llm = ChatOpenAI(model="gpt-4o-mini")

# Get Jina API key from environment
JINA_API_KEY = os.getenv('JINA_API_KEY')
if not JINA_API_KEY:
    raise ValueError("JINA_API_KEY environment variable is required")


# class Status(BaseModel):
#     job_posting_found: bool = Field(default=False, description="Whether a job posting was found on the webpage")
#     job_posting_link: List[str] = Field(default=[], description="Links to job postings found on the webpage")

#     class Config:
#         arbitrary_types_allowed = True


# class AgentState(MessagesState):
#     final_response: Status


repl = PythonREPL()

@tool
def python_repl_tool(code: Annotated[str, "Python code to run"]):
    """Use this to execute python code. If you want to see the output of a value,
    you should print it out with `print(...)`. This is visible to the user."""
    try:
        result = repl.run(code)
    
    except BaseException as e:
        return f"Failed to run code: {e}"

    result_str = f"Successfully executed:\n```python\n{code}\n```\nStdout: {result}"
    return (result_str + "\n\nIf you have found a detailed job posting, respond with JOB POSTING FOUND")

jina_reader = """
Given a url, the agent scrapes through the website and outputs the content of the webpage

def jina_reader(url: str) -> str:
    url = f'https://r.jina.ai/{url}'
    headers = {
        'Authorization': f'Bearer jina_07a87e31418c4dd0b33f7d74f64a0290zJCI8gIFlb6os-oyzvMqchkpRbeQ'
    }

    response = requests.get(url, headers=headers)
    return response.text
"""

SYSTEM_PROMPT = f"""You are a helpful AI assistant that helps people find jobs. You will be given a url and a search tool called jin_reader. You can help me find jobs by indicating if a webpage contains a job posting or not. Note that some pages might have links to job postings, but the page itself might not contain the job posting. In such cases, you can indicate that the page contains a link to one or more job postings, but not the job posting itself. If the page contains links to job postings, return those links in a list. You can also indicate if the page does not contain a job posting. If you have found a detailed job posting, respond with JOB POSTING FOUND. You can also use the python_repl_tool to run the following code: {jina_reader}"""

class JobFinder:
    def __init__(self):
        self.agent = create_react_agent(
            llm, 
            tools=[python_repl_tool],
            state_modifier=SYSTEM_PROMPT
        )
    
    def get_next_node(self, last_message: BaseMessage, goto: str):
        print(last_message.content)
        if "JOB POSTING FOUND" in last_message.content:  # job posting found
            # job posting found
            return END
        return goto
    
    def run(self, state: MessagesState) -> Command[Literal["job_finder", END]]:
        result = self.agent.invoke(state)
        goto = self.get_next_node(result["messages"][-1], "job_finder")

        result["messages"][-1] = HumanMessage(
            content=result["messages"][-1].content, 
            name="job_finder"
        )

        return Command(
            update={
                "messages": result["messages"],
            },
            goto=goto,
        )
