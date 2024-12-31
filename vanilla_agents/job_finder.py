"""
Given a url, the agent scrapes through the website and outputs the content of the webpage containing the job details.
Uses Jina AI to read the content of the webpage.
"""

from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
import requests
import json

load_dotenv()


SYSTEM_PROMPT = """You are a helpful AI assistant that assists people in identifying job postings from provided webpage content. There might be job postings with detailed information, links to job postings, or no job postings at all. A job description is considered detailed only if it provides essential information such as roles, responsibilities and skills. Check the content of the webpage first for detailed job descriptions and then for links to job postings. Make sure to check thoroughly and provide accurate results. Your task is to carefully analyze the content and determine the following:

1. Whether the content contains a job posting with detailed information (e.g., job title, description, requirements, etc.).
   - If a job posting is found, indicate that a job posting was found by returning `True` for `job_posting_found`.
   - Sometimes there might be multiple job postings but only with brief details. Check if there are links to the detailed job postings in such cases.

2. If no job posting is found in the content, determine whether it contains one or more links to job postings.
   - If links to job postings are found, return those links as a list in the `job_posting_link` field.
   - If no job posting and no links to job postings are found, return an empty list for `job_posting_link`.

3. If the page does not contain a job posting or links to job postings, return `False` for `job_posting_found` and an empty list for `job_posting_link`.

Your response must adhere to the structure defined in the `ValidationResponse` class:
- `job_posting_found`: Boolean indicating if a job posting was found. Returns `True` ONLY if a detailed job description was found. If no job posting was found or links to job postings were found, return `False`.
- `job_posting_link`: List of links to job postings if available; otherwise, an empty list."""

def jina_reader(url: str) -> str:
    url = f'https://r.jina.ai/{url}'
    headers = {
        'Authorization': f'Bearer jina_07a87e31418c4dd0b33f7d74f64a0290zJCI8gIFlb6os-oyzvMqchkpRbeQ',
        'X-Return-Format': 'markdown'
    }

    response = requests.get(url, headers=headers)
    return response.text


class ValidationResponse(BaseModel):
    job_posting_found: bool = Field(..., description="Whether a job posting with details was found on the webpage. Returns True if a job posting was found, False otherwise")
    job_posting_link: List[str] = Field(..., description="If a job posting was NOT found but a possible link to a job posting was found, it must be included here. Otherwise, return an empty list")

def validate(url: str):
    """Validates the content of the webpage to check if it contains job details"""

    site_content = jina_reader(url)
    
    client = OpenAI()
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": site_content}
            ],
            response_format=ValidationResponse
    )
    response = response.choices[0].message.parsed.model_dump()

    status = response["job_posting_found"]
    links = response["job_posting_link"]

    validation = {
        "url": url,
        "links": links,
        "site_content": site_content
    }

    # Case 1: Job posting found
    if status == True and links == []:
        validation["status"] = 1
    
    # Case 2: No job posting found but possible links to job postings found
    elif status == False and links != []:
        print("No job posting found but possible links to job postings found")
        validation["status"] = 2
    
    # Case 3: Both job posting and links to job postings not found
    elif status == True and links != []:
        print("Job posting found and possible links to job postings found")
        validation["status"] = 3

    # Case 4: No job posting or possible links to job postings found. Dead end.
    elif status == False and links == []:
        print("No job posting or possible links to job postings found")
        validation["status"] = 4

    # Read existing content or create new structure
    try:
        with open('./data/jps_found.json', 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {"jobs_found": []}
    except FileNotFoundError:
        data = {"jobs_found": []}

    # Append new validation
    data["jobs_found"].append(validation)

    # Write updated content back to file
    with open('./data/jps_found.json', 'w') as f:
        json.dump(data, f, indent=2)
        
    return validation
     
# recursively call validate() until status == 4 for all links
def recursive_validate(url: str, found_jobs=None, processed_urls=None):
    if found_jobs is None:
        found_jobs = []
    if processed_urls is None:
        processed_urls = set()
    
    # Skip if URL was already processed
    if url in processed_urls:
        return found_jobs
    
    processed_urls.add(url)
    result = validate(url)
    
    # Base cases
    if result["status"] == 1 or result["status"] == 3:  # Job posting found (with or without additional links)
        found_jobs.append(result)
        
        # If status is 3, continue processing the additional links
        if result["status"] == 3:
            print(f"++Found job posting and {len(result['links'])} additional links++")
            for link in result["links"]:
                recursive_validate(link, found_jobs, processed_urls)
        return found_jobs
    elif result["status"] == 4:  # Dead end
        return found_jobs
        
    # Recursive case: process all links (status 2)
    if result["links"]:
        print(f"++Recursively validating {len(result['links'])} links++")
        for link in result["links"]:
            recursive_validate(link, found_jobs, processed_urls)
    
    return found_jobs

if __name__ == "__main__":
    jobs = recursive_validate("https://www.ycombinator.com/companies/hyperdx/jobs")
    print(f"\nFound {len(jobs)} job postings:")
    for i, job in enumerate(jobs, 1):
        print(f"{i}. Job URL: {job['url']}")
