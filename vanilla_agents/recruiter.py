"""
Reaches out to potential candidates via email and tries to get them to apply for a job.
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

