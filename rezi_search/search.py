"""
Uses rezi search to search for top candidates when given a query
"""

import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

BEARER_TOKEN = os.getenv("SEARCH_BEARER_TOKEN")
SEARCH_URL = os.getenv("SEARCH_URL")
ORG_ID = os.getenv("ORG_ID")

headers = {
  'Organization-Id': ORG_ID,
  'Content-Type': 'application/json',
  'Authorization': f'Bearer {BEARER_TOKEN}'
}

class SearchRequest:
    def __init__(self, query):
        self.query = query


    def _get_resume_ids(self, response):
        response = json.loads(response)
        results = response["data"]["es_results"]["hits"]["hits"]

        rids = []
        for hit in results:
            rids.append(hit["_id"])
        return rids

    def search(self):
        payload = json.dumps({
            "search": self.query,
        })
        response = requests.request("POST", SEARCH_URL, headers=headers, data=payload)
        return self._get_resume_ids(response.text)
    

if __name__ == "__main__":
    q = "React Developer"
    x = SearchRequest(q)
    print(x.search())