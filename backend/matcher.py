import json

with open("data/resume.json") as f:
    resume = json.load(f)

with open("data/jd.json") as f:
    jd = json.load(f)

resume_skills = set(
    skill.lower()
    for skill in resume["skills"]
)

required_skills = set(
    skill.lower()
    for skill in jd["required_skills"]
)

matches = resume_skills.intersection(
    required_skills
)

score = (
    len(matches)
    / len(required_skills)
) * 100

print("Match Score:", round(score, 2))
print()

print("Matched Skills:")
for skill in matches:
    print("-", skill)