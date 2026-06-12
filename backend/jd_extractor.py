import json

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

with open("data/jd.txt", "r") as f:
    jd_text = f.read()

prompt = f"""
Extract information from this job description.

Return ONLY valid JSON.

Schema:

{{
    "job_title": "",
    "required_skills": [],
    "responsibilities": []
}}

Job Description:

{jd_text}
"""

response = llm.invoke([
    HumanMessage(content=prompt)
])

content = response.content
content = content.replace("```json", "")
content = content.replace("```", "")
content = content.strip()

with open("data/jd.json", "w") as f:
    f.write(content)

print(content)