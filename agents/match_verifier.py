"""
After rezi-search delivers top candidates for a given job, the verifier will be responsible for validating the candidates based on the job posting. The verifier will check if the candidate is a good fit for the job based on the following criteria:
- Job fit
- Location feasibility
"""
from openai import OpenAI
import requests
import json
from pydantic import BaseModel, Field
from typing import List, Dict


def validate(job_posting: str):
        """
        Validate the candidate based on the job posting. Return if the candidate is a good fit or not along with the reasons.
        """
        pass