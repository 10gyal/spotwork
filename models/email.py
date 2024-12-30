"""
Reaches out to potential candidates via email and tries to get them to apply for a job.
"""
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
import requests
import json

load_dotenv()


class EmailContent(BaseModel):
    subject: str = Field(..., title="Subject of the email")
    salutation: str = Field(..., title="Salutation of the email")
    body: str = Field(..., title="Body of the email")


class Email:
    def __init__(self, sender: str, receiver: str):
        self.sender = sender
        self.receiver = receiver

    def _get_email_thread(self):
        """
        Get the email thread from the database.
        """
        pass

    def compose_email(self):
        """
        Compose the email based on the email thread.
        """
        pass

    def send(self, email_content: EmailContent):
        """
        Send the email to the receiver.
        """
        pass