"""
Given a job posting taken from a webpage, the curator will deliver a clean job posting that is ready for Elastic Search
"""

from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
import requests
import json


load_dotenv()


class CuratedResponse(BaseModel):
    curated_content: str = Field(..., description="The curated job posting extracted from the webpage content.")


SYSTEM_PROMPT = """You are a specialized AI assistant. You receive raw text from a scraped job posting page, which may include extraneous details like images, links, or irrelevant marketing statements. Your goal is to create a clean, concise job posting that includes only the essential information necessary for a candidate to understand the role at a glance.

1. Essential Details to Include (where applicable):
- Job Title
- Company Name
- Job Location(s) (city, state, remote, etc.)
- Salary or Compensation Range (if provided)
- Equity Range (if provided)
- Key Responsibilities (a short summary)
- Key Requirements / Qualifications
- Any Important Notes on Work Environment (e.g., remote vs. on-site, travel requirements, etc.)
- How to Apply (if directly stated in the text; otherwise omit)

2. Details to Exclude or Remove:
- Hyperlinks (unless they are the direct application link)
- References to images or media
- Long-winded marketing copy, branding statements, or tangential content
- Excessive founder bios, or background information not relevant to the role
- Any personally identifiable information (PII) unless it’s essential to the job itself

3. Formatting Guidelines:
- Present the final job description in clear, plain text or simple markdown.
- Use short headings or bullet points for readability.
- The output should be self-contained and free of content unrelated to the actual job (e.g., disclaimers about scraping, references to images, etc.).

4. Example:
- Job Title: Founding AI Engineer
- Company: Harper
- Location: San Francisco, CA (On-site/Remote Hybrid)
- Compensation: $100K–$180K base + 0.5%–2.5% equity
- Responsibilities: Develop and deploy AI systems for commercial insurance, manage large-scale data flows, etc.
- Requirements: Experience with modern AI/ML stack, shipping production AI, comfort with rapid iteration, etc.
- How to Apply: [Include direct application link if explicitly stated]

Your response must strictly adhere to these guidelines, providing only the most pertinent details for potential job applicants and nothing else. The goal is to produce a succinct, professional job posting that a candidate can quickly review and understand.
"""

def curate(content: str) -> str:
    client = OpenAI()
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": content}
            ],
            response_format=CuratedResponse
    )

    response = response.choices[0].message.parsed.model_dump()

    return response["curated_content"]


if __name__ == "__main__":
    ## read content from validation.json
    with open('validation.json', 'r') as f:
        content = json.load(f)
        curated_content = {
            "url": content["url"],
            "curated_content": curate(content["site_content"])
        }
        # save curated content to curated.json
        with open('curated.json', 'a') as f:
            json.dump({"curated_content": curated_content}, f, indent=2)


