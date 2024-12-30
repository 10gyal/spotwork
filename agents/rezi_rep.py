"""
Reaches out to the hiring company to ask if they would like to be introduced to a potential candidate. The goal is to convince that the candidate is a good fit for the job.
- Conduct a brief research on the company and the job posting to make the email more personalized. 
- Use the candidate's resume to highlight their skills and experience.
"""
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
import requests
import json
from tools.email import Email

load_dotenv()


