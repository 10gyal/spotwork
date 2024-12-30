from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv

class Candidate:
    def __init__(self, id):
        self.id = id
    
    def get_resume(self):
        """
        Get the resume from db and reconstruct it into a string. Must include everything that the actual resume would have.
        """
        pass

    def get_user_info(self):
        """
        Get the user information from the database. Mainly for the name and email.
        """
        pass
