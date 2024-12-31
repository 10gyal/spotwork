from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
from firestore import FirestoreClient

load_dotenv()

class Candidate:
    def __init__(self, resume_id):
        self.resume_id = resume_id
        self.client = FirestoreClient.get_instance()

    def get_data(self):
        """
        Get the resume from db and reconstruct it into a string. Must include everything that the actual resume would have.
        """
        data = self.client.get_resume_by_id(self.resume_id)
        resume = self._get_resume()
        user_info = self._get_user_info()

        return data

    def _get_resume(self):
        """
        Get the resume data from the retrieved data.
        """
        pass

    def _get_user_info(self):
        """
        Get the user information. Mainly for the name and email.
        """
        pass


if __name__ == "__main__":
    c = Candidate("006CK3pwiGdp0DhSsKTM")
    print(c.get_data())
