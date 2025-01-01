# Rezi Agent
### JP Curation
- Get a bunch of links/jps from HackerNews
- Recursively obtain the actual job descriptions from each posts using JinaAI
- Curate the job descriptions to keep only the essential informaiton
- This curated jp is ready to be used as a query in Elastic Search (ES)

### Search
- Establish connection to ES
- Feed the curated JPs into ES
- Retrieve Results + User contact information
- Retrieve Recruiting company contact information
- Verify the top candidates from ES with the actual JP

### Communication
- Email the top selected candidates if they would like to be connected to the recruiting company
- Email the recruiting company if they would like to see the resumes of some potential candidates
- Once either of the parties agree, human enters the loop
