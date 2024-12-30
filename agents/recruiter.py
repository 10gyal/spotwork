"""
Reaches out to potential candidates via email and tries to get them to apply for a job.
"""
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
import requests
import json
from tools.email import Email

load_dotenv()

