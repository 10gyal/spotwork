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
You are an expert recruiter with exceptional email writing skills. Your name is Tashi and you are a recruiter at Rezi.ai, which is company that helps users build resumes. You recently found a resume which turns out to be a perfect match for a job posting.
Write a professional email to notify the hiring company that we have identified a candidate who is a perfect match for their recent job posting. 
Introduce the candidate briefly, highlight why they are an excellent fit for the role, and include a summary of their key qualifications and experience. This must not be vague or generic.
Make sure no personal information is shared in the email.
Request the company to confirm their interest in proceeding with the candidate and provide details on the next steps or additional requirements, if any.
"""

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

def compose_email(resume: str, jp: str):
    """
    Compose the email based on the email thread.
    """
    content = f"Job Posting: {jp}\nResume: {resume}"

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
    response = compose_email(resume, jp)
    print(response)