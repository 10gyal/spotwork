"""
NOT USED
"""
import requests
import json
from datetime import datetime

def fetch_job_details():
    """Fetch all job postings from HN API and save as JSON"""
    base_url = "https://hacker-news.firebaseio.com/v0"
    
    # Get list of job IDs
    response = requests.get(f"{base_url}/jobstories.json")
    response.raise_for_status()
    job_ids = response.json()
    
    jobs_data = []
    for job_id in job_ids:
        # Fetch job data
        response = requests.get(f"{base_url}/item/{job_id}.json")
        response.raise_for_status()
        job_data = response.json()
        jobs_data.append(job_data)
    
    # Save to JSON file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"./data/hn_jobs_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(jobs_data, f, indent=2)
    
    print(f"Saved {len(jobs_data)} jobs to {filename}")

if __name__ == "__main__":
    fetch_job_details()
