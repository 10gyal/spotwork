"""
Uses rezi search to search for top candidates when given a query
"""

import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

AUTH_URL = os.getenv("AUTH_URL")
AUTH_EMAIL = os.getenv("AUTH_EMAIL")
AUTH_PASSWORD = os.getenv("AUTH_PASSWORD")
SEARCH_URL = os.getenv("SEARCH_URL")
ORG_ID = os.getenv("ORG_ID")

def get_bearer_token():
    try:
        
        payload = json.dumps({
        "email": AUTH_EMAIL,
        "password": AUTH_PASSWORD,
        "returnSecureToken": True
        })
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", AUTH_URL, headers=headers, data=payload)

        print("="*50, "AUTHENTICATION SUCCESSFUL", "="*50)
        return response.json().get("idToken")
    except Exception as e:

        print(e)

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
        headers = {
            'Organization-Id': ORG_ID,
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {get_bearer_token()}'
        }
        payload = json.dumps({
            "search": self.query,
        })
        response = requests.request("POST", SEARCH_URL, headers=headers, data=payload)
        return self._get_resume_ids(response.text)
    

if __name__ == "__main__":
    q = "React Developer"
    x = SearchRequest(q)
    print(x.search())
    