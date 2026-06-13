import json
import os

from dotenv import load_dotenv
from langfuse import observe
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

from embeddings import get_embedding
from vector_store import collection

load_dotenv()

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

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

@observe(name="evaluate_candidate")
def evaluate_candidate(candidate_profile):
    prompt = f"""
    You are an expert technical recruiter.

    JOB DESCRIPTION:

    {query_text}

    CANDIDATE PROFILE:

    {candidate_profile}

    Return ONLY valid JSON.

    Format:

    {{
        "match_score": number,
        "matching_skills": [],
        "Missing_skills": [],
        "strengths": [],
        "weaknesses": [],
        "recommendation": ""
    }}
    """

    response = llm.invoke(
        [HumanMessage(content=prompt)]
    )

    result = response.content

    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()

    evaluation = json.loads(result)
    print(f"Match score: {evaluation.get('match_score')}")
    
    return evaluation


from retrieve import get_top_candidate

if __name__ == "__main__":

    candidate_profile = get_top_candidate()

    evaluation = evaluate_candidate(
        candidate_profile
    )

    print(
        json.dumps(
            evaluation,
            indent=4
        )
    )