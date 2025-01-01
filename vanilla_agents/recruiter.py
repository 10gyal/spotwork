"""
Reaches out to potential candidates via email and tries to get them to apply for a job.
"""
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
import requests
import json
from models import candidate, email

load_dotenv()

SYSTEM_PROMPT = """
You are an expert recruiter with exceptional email writing skills. Your name is Tashi and you are a recruiter at Rezi.ai, which is company that helps users build resumes. You recently found a job posting for which a user's resume is a perfect match. Write a professional email to reach out to the candidate whose resume is a perfect match for the job posting. You will be given the candidate's name, resume and the job posting details. You are to convince the candidate to apply for the job. Explain why you think the candidate is a perfect fit for the job and why they should consider applying. Make sure the email is professional yet original and organic. However, do not provide any methods on how to apply. This email is only to convince the candidate to apply for the job."""

class EmailContent(BaseModel):
    email_content: str = Field(..., title="Content of the email")

def get_user_info(candidate_id: str):
    """
    Get the user information from the database.
    """
    pass

def get_email_thread():
    """
    Get the email thread from the database. Implement later.
    """
    pass

def compose_email(user_name: str, resume: str, jp: str):
    """
    Compose the email based on the email thread.
    """
    content = f"Candidate Name: {user_name}\n\nJob Posting: {jp}\nResume: {resume}"

    client = OpenAI()
    response = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            max_tokens=8000,
            messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": content}
            ],
            response_format=EmailContent
    )

    response = response.choices[0].message.parsed.model_dump()

    return response

def send_email(email_content):
    """
    Send the email to the receiver.
    """
    pass

if __name__ == "__main__":
    with open("./data/curated_jps.json") as f:
        job_posting = json.load(f)
    jp = job_posting["jobs"][2]["curated_content"]
    candidate = candidate.Candidate("kxHvSjo7RRlahk9T3wAp")
    resume = candidate.get_resume()
    user_name = candidate.get_user_info()["name"]
    response = compose_email(user_name, resume, jp)
    print(response)