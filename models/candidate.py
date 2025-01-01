from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
from firestore import FirestoreClient
import json

load_dotenv()

class Candidate:
    def __init__(self, resume_id):
        self.resume_id = resume_id
        self.client = FirestoreClient.get_instance()
        self.data = self.client.get_resume_by_id(self.resume_id)

    def get_resume(self):
        """
        Get the resume data from the retrieved data. Reconstruct the resume into a single string.
        """
        data = json.loads(self.data).get("data")
        summary = data.get("summary", "").get("summary")
        experience = data.get("experience")
        education = data.get("education")

        exps = ""
        # experience is a dict with key = exp_id and value = dict containing e_index. order by the key e_index
        for exp_id, exp in sorted(experience.items(), key=lambda x: x[1].get("index")):
            index = exp.get("index", "")
            role = exp.get("role", "")
            company = exp.get("company", "")
            duration = exp.get("duration", "")
            location = exp.get("location", "")
            description = exp.get("description", "")
            exps += f"{index+1}. {role}\n{company} | {duration}, {location}\n{description}\n\n"

        edus = ""
        # education is a dict with key = edu_id and value = dict containing e_index. order by the key e_index
        for edu_id, edu in sorted(education.items(), key=lambda x: x[1].get("index")):
            qualification = edu.get("qualification", "")
            institution = edu.get("institution", "")
            date = edu.get("date", "")
            location = edu.get("location", "")
            edus += f"{qualification}\n{institution} | {date}, {location}\n\n"

        resume = f"Summary\n{summary}\n\nExperience\n{exps}Education\n{edus}"
        return resume


    def get_user_info(self):
        """
        Get the user information. Mainly for the name and email.
        """
        # return a dict with keys: name, email, linkedin, phone, website
        data = json.loads(self.data).get("data")
        contact = data.get("contact")
        name = contact.get("name", "")
        email = contact.get("email", "")
        linkedin = contact.get("linkedin", "")
        phone = contact.get("phone", "")
        website = contact.get("website", "")

        return {
            "name": name,
            "email": email,
            "linkedin": linkedin,
            "phone": phone,
            "website": website
        }

if __name__ == "__main__":
    c = Candidate("006CK3pwiGdp0DhSsKTM")
    print(c.data)
    print(c.get_resume())
    print(c.get_user_info())
