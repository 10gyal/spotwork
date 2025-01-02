from vanilla_agents.job_finder import recursive_validate
from vanilla_agents.post_curator import curate
import json
from typing import List, Dict
import os

def process_job_postings(url: str) -> List[Dict]:
    """
    Process job postings by first finding them and then curating them.
    
    Args:
        url: Starting URL to search for job postings
        
    Returns:
        List of dictionaries containing processed job postings with their URLs and curated content
    """
    # First, find all job postings
    print("Finding job postings...")
    jobs = recursive_validate(url)
    
    if not jobs:
        print("No job postings found.")
        return []
    
    print(f"\nFound {len(jobs)} job postings. Curating content...")
    
    # Process each job posting
    curated_jobs = []
    for job in jobs:
        curated_content = curate(job['site_content'])
        curated_jobs.append({
            "url": job['url'],
            "curated_content": curated_content
        })
        
    # Save all curated jobs to a single file
    output_file = './data/curated_jps.json'
    with open(output_file, 'w') as f:
        json.dump({"jobs": curated_jobs}, f, indent=2)
    
    print(f"Curated {len(curated_jobs)} jobs. Results saved to {output_file}")
    return curated_jobs

if __name__ == "__main__":
    # Example usage with a starting URL
    starting_url = "https://news.ycombinator.com/item?id=42455372"
    processed_jobs = process_job_postings(starting_url)
    
    # Display results
    if processed_jobs:
        print("\nProcessed Job Postings:")
        for i, job in enumerate(processed_jobs, 1):
            print(f"\n{i}. Job URL: {job['url']}")
            print("Curated Content:")
            print(job['curated_content'])
 