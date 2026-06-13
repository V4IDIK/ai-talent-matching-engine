import json
import os

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

from embeddings import get_embedding
from vector_store import collection

load_dotenv()

# Load JD
with open("data/jd.json", "r") as f:
    jd = json.load(f)

query_text = f"""
Job Title:
{jd.get("job_title", "")}

Required Skills:
{", ".join(jd.get("required_skills", []))}

Responsibilities:
{" ".join(jd.get("responsibilities", []))}
"""

query_embedding = get_embedding(query_text)

# Retrieve top candidate
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=1
)

candidate_profile = results["documents"][0][0]

# Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

prompt = f"""
You are an expert technical recruiter.

JOB DESCRIPTION:

{query_text}

CANDIDATE PROFILE:

{candidate_profile}

Evaluate the candidate and provide:

1. Match Score (0-100)
2. Matching Skills
3. Missing Skills
4. Strengths
5. Weaknesses
6. Final Recommendation

Keep the response concise and professional.
"""

response = llm.invoke(
    [HumanMessage(content=prompt)]
)

print("\nAI EVALUATION REPORT\n")
print(response.content)