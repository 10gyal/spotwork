"""
After rezi-search delivers top candidates for a given job, the validator will be responsible for validating the candidates. It must check the following:
- Job fit
- Location feasibility
"""
from openai import OpenAI
import requests
import json
from pydantic import BaseModel, Field
from typing import List, Dict


class Candidate:
    def __init__(self, id):
        self.id = id
    
    def get_resume(self):
        """
        Get the resume from db and reconstruct it into a string. Must include everything that the actual resume would have.
        """
        pass

    def validate(self, job_posting: str):
        """
        Validate the candidate based on the job posting. Return if the candidate is a good fit or not along with the reasons.
        """
        pass