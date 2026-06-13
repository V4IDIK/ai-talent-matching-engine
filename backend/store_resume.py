import json

from embeddings import get_embedding
from vector_store import collection

with open("data/candidate_1.json", "r") as f:
    resume = json.load(f)

candidate_name = resume["name"]

# ---------- Skills ----------
skills_text = ", ".join(resume.get("skills", []))

# ---------- Projects ----------
projects_text = []

for project in resume.get("projects", []):
    projects_text.append(
        f"""
        Title: {project.get('title', '')}
        Technologies: {', '.join(project.get('tech_stack', []))}
        Description: {project.get('description', '')}
        """
    )

projects_text = "\n".join(projects_text)

# ---------- Experience ----------
experience_text = []

for exp in resume.get("experience", []):
    experience_text.append(
        f"""
        Company: {exp.get('company', '')}
        Role: {exp.get('title', '')}
        Description: {' '.join(exp.get('description', []))}
        """
    )

experience_text = "\n".join(experience_text)

# ---------- Education ----------
education_text = []

for edu in resume.get("education", []):
    education_text.append(
        f"""
        Institution: {edu.get('institution', '')}
        Degree: {edu.get('degree', '')}
        """
    )

education_text = "\n".join(education_text)

resume_text = f"""
Candidate: {candidate_name}

Skills:
{skills_text}

Projects:
{projects_text}

Experience:
{experience_text}

Education:
{education_text}
"""

embedding = get_embedding(resume_text)

candidate_id = candidate_name.lower().replace(" ", "_")

existing = collection.get(
    ids=[candidate_id]
)

if existing["ids"]:
    print(
        f"{candidate_name} already exists."
    )
    exit()

collection.add(
    ids=[candidate_id],
    documents=[resume_text],
    embeddings=[embedding],
    metadatas=[{
        "name": candidate_name,
        "skills_count": len(resume.get("skills", [])),
        "projects_count": len(resume.get("projects", [])),
        "experience_count": len(resume.get("experience", []))
    }]
)

print(f"Stored {candidate_name}")
print(f"Total resumes: {collection.count()}")