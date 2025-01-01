"""
After rezi-search delivers top candidates for a given job, the verifier will be responsible for validating the candidates based on the job posting. The verifier will check if the candidate is a good fit for the job based on the following criteria:
- Job fit
- Location feasibility
Returns:

"""
from openai import OpenAI
import requests
import json
from pydantic import BaseModel, Field
from typing import List, Dict
from models import candidate


SYSTEM_PROMPT = """You are a specialized AI assistant. You will receive a job posting and a resume. Your goal is to determine if the candidate is a good fit for the job based on the job posting. Candidate fit is measured on a scale from 1-5 where 5 is the perfect fit. You should consider the candidate's skills, experience, qualifications and location feasibility in relation to the job requirements. Provide a clear and concise response indicating whether the candidate is a good fit for the job and include reasons to support your decision."""


class ValidationResponse(BaseModel):
        fit_score: int = Field(..., description="On a scale of 1-5, where 1 is not a good fit and 5 is a perfect fit, how well does the candidate fit the job posting?")
        reasons: str = Field(..., description="Reasons why the candidate is a good fit or not.")

def validate(job_posting: str, resume: str) -> Dict:
        """
        Validate the candidate based on the job posting. Return if the candidate is a good fit or not along with the reasons.
        """
        content = f"Job Posting: {job_posting}\nResume: {resume}"

        client = OpenAI()
        response = client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                max_tokens=8000,
                messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": content}
                ],
                response_format=ValidationResponse
        )

        response = response.choices[0].message.parsed.model_dump()

        return response

if __name__ == "__main__":
        with open("./data/curated_jps.json") as f:
                job_posting = json.load(f)
        jp = job_posting["jobs"][2]["curated_content"]
        resume = candidate.Candidate("kxHvSjo7RRlahk9T3wAp").get_resume()
        # print(resume)
        response = validate(jp, resume)
        print(response)
        