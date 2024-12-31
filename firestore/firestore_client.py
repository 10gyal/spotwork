import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from typing import Optional, Dict, List, Tuple, Any
from dotenv import load_dotenv
import os
from datetime import datetime
import json
import base64

load_dotenv()

firebase_config_b64 = os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY')

class FirestoreError(Exception):
    """Base exception class for Firestore operations."""
    pass

class FirestoreClient:
    _instance: Optional['FirestoreClient'] = None
    _db: Optional[firestore.Client] = None

    def __init__(self):
        """Initialize Firebase Admin SDK and get Firestore client."""
        try:
            if not firebase_admin._apps:
                if not firebase_config_b64:
                    raise FirestoreError("Firebase service account key not found in environment variables")
                firebase_config = json.loads(base64.b64decode(firebase_config_b64))
                cred = credentials.Certificate(firebase_config)
                firebase_admin.initialize_app(cred)
            
            self._db = firestore.client()
        except Exception as e:
            raise FirestoreError(f"Failed to initialize Firestore client: {type(e).__name__}: {str(e)}") from e
    
    @classmethod
    def get_instance(cls) -> 'FirestoreClient':
        """Get singleton instance of FirestoreClient."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def get_resumes_collection(self) -> firestore.CollectionReference:
        """Get reference to resumes collection."""
        if not self._db:
            raise FirestoreError("Firestore client not initialized")
        return self._db.collection('resumes')
    
    def get_resume_by_id(self, resume_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch a specific resume by ID.
        
        Args:
            resume_id: The ID of the resume to fetch
            
        Returns:
            The resume data as a dictionary if found, None otherwise
            
        Raises:
            FirestoreError: If there's an error fetching the resume
        """
        try:
            doc = self.get_resumes_collection().document(resume_id).get().to_dict()
            return json.dumps(doc, indent=4)
        
        except Exception as e:
            raise FirestoreError(f"Failed to fetch resume {resume_id}: {type(e).__name__}: {str(e)}") from e
    

if __name__ == "__main__":
    client = FirestoreClient.get_instance()
    resume = client.get_resume_by_id('006CK3pwiGdp0DhSsKTM')
    print(resume)
