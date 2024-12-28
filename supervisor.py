import os
import time
from concurrent.futures import ThreadPoolExecutor
from .agents import JobFinder
from langgraph.graph import StateGraph, START
from IPython.display import Image, display


class SupervisingAgent:
    def __init__(self):
        pass

    def run(self):
        # Initialize agents
        job_finder = JobFinder()

        # Create a Langchain workflow
        workflow = StateGraph()

        # Add nodes for each agent
        workflow.add_node("find_job", job_finder.run)

        # Set up the edges
        workflow.add_edge(START, "find_job")
        workflow.compile()


