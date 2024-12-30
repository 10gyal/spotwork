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
from models.email import Email

load_dotenv()

def get_job_posting():
    """
    Get the job posting from the database.
    """
    pass

def get_resume(candidate_id: str):
    """
    Get the resume from the database.
    """
    pass

def get_user_info(candidate_id: str):
    """
    Get the user information from the database.
    """
    pass

def get_company_info():
    """
    Get the company information from the database.
    """
    pass

def get_email_thread():
    """
    Get the email thread from the database.
    """
    pass

def compose_email(email_content):
    """
    Compose the email based on the email thread.
    """
    pass

def send_email(email_content):
    """
    Send the email to the receiver.
    """
    pass