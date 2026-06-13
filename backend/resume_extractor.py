import os
import json

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

with open("data/candidate_1.txt", "r") as f:
    resume_text = f.read()

prompt = f"""
Extract the following information from this resume.

Return ONLY valid JSON.

Schema:

{{
  "name": "",
  "skills": [],
  "projects": [],
  "experience": [],
  "education": []
}}

Resume:

{resume_text}
"""

response = llm.invoke([
    HumanMessage(content=prompt)
])

content = response.content

content = content.replace("```json", "")
content = content.replace("```", "")
content = content.strip()

with open("data/candidate_1.json", "w") as f:
    f.write(content)

print("Saved to data/candidate_1.json")