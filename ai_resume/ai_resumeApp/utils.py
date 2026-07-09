import pytesseract
from pdf2image import convert_from_path

def extract_text(file):
    text = ""
    # PDF को images में convert करो
    pages = convert_from_path(file.temporary_file_path())
    for page in pages:
        # OCR से text निकालो
        page_text = pytesseract.image_to_string(page)
        text += page_text + " "
    return text

# 🔹 Clean text
def clean_text(text):
    return text.lower()

def detect_role_from_jd(job_desc):

    # 🔥 normalize text
    job_desc = job_desc.lower()
    job_desc = job_desc.replace("-", " ")

    # 🔹 Data Analyst
    if "data analyst" in job_desc or "analytics" in job_desc:
        return "Data Analyst"

    # 🔹 Python Developer
    elif "python developer" in job_desc or "django" in job_desc or "flask" in job_desc:
        return "Python Developer"

    # 🔹 Full Stack
    elif "full stack" in job_desc or "fullstack" in job_desc:
        return "Full Stack Developer"

    # 🔹 MERN
    elif "mern" in job_desc or "mern stack" in job_desc:
        return "Mern Stack Developer"

    # 🔹 Frontend
    elif "frontend" in job_desc or "react" in job_desc:
        return "Frontend Developer"

    # 🔹 Backend
    elif "backend" in job_desc or "node" in job_desc:
        return "Backend Developer"

    # 🔹 ML
    elif "machine learning" in job_desc or "deep learning" in job_desc:
        return "ML Engineer"

    # 🔹 Web Developer
    elif "web developer" in job_desc:
        return "Web Developer"

    else:
        return "General Role"
from fuzzywuzzy import fuzz

def extract_skills(text):
    skills_list = ["python", "django", "sql", "html", "css", "javascript", "power bi","tableau"]

    found = []
    missing = []

    for skill in skills_list:
        score = fuzz.partial_ratio(skill, text.lower())
        if score >= 70:   # threshold for found
            found.append(skill)
        else:
            missing.append(skill)

    return found, missing

ROLE_KEYWORDS = {
    "Python Developer": [
        "python",
        "django",
        "flask",
        "sql"
        
    
    ],

    "Data Analyst": [
        "sql",
        "power bi",
        "excel",
        "pandas",
        "numpy",
        "python",
        "tableau"
    ],

    "Frontend Developer": [
        "html",
        "css",
        "javascript",
        "react",
        "reactjs"
    ],

    "Backend Developer": [
        "node",
        "nodejs",
        "express",
        "expressjs",
        "django",
        "flask"
    ],

   
    "Mern Stack Developer": [

    "react",

    "node",

    "express",

    "mongodb",

    "javascript"
],


    "Full Stack Developer": [
        "html",
        "css",
        "javascript",
        "react",
        "node",
        "mongodb",
        "django",
        "sql"
    ]
}
def detect_role(text):

    text = text.lower()

    detected_roles = {}
    found_skills = []

    skip_duplicates = {
        "reactjs": "react",
        "nodejs": "node",
        "expressjs": "express",
        "mongo": "mongodb"
    }

    for role, keywords in ROLE_KEYWORDS.items():

        matched = []

        for skill in keywords:

            if skill in text:

                main_skill = skip_duplicates.get(skill, skill)

                if main_skill not in matched:
                    matched.append(main_skill)

        if matched:
            detected_roles[role] = len(matched)
            found_skills.extend(matched)

    found_skills = list(set(found_skills))

    if detected_roles:
        best_role = max(detected_roles, key=detected_roles.get)
    else:
        best_role = "General Role"

    return best_role, found_skills

def match_keywords(resume_text, role):

    required_skills = ROLE_KEYWORDS.get(role, [])

    found_skills = []
    missing_skills = []

    text = resume_text.lower()

    skill_groups = {

        "react": ["react", "reactjs", "react js"],

        "node": ["node", "nodejs", "node js"],

        "express": ["express", "expressjs", "express js"],

        "mongodb": ["mongodb", "mongo"],
        
        "javascript": ["javascript", "js"],

        "sql" :["sql","mysql"]

        # "fastapi": ["fastapi","fast api"]

        # "rest api":["rest api","restapi","api"]

    }

    checked = set()

    for main_skill, variations in skill_groups.items():

        if not any(v in required_skills for v in variations):
            continue

        found = False

        for variation in variations:

            if variation in text:

                found = True
                break

        if found:
            found_skills.append(main_skill)

        else:
            missing_skills.append(main_skill)

        checked.update(variations)

    for skill in required_skills:

        if skill in checked:
            continue

        if skill.lower() in text:

            found_skills.append(skill)

        else:

            missing_skills.append(skill)

    return list(set(found_skills)), list(set(missing_skills))
# 🔹 ATS Score

def calculate_score(found, total):
    if len(total) == 0:
        return 0
    return round((len(found) / len(total)) * 100, 2)

# 🔹 Missing skills
def missing_skills(found, total):
    return list(set(total) - set(found))


# 🔹 Suggestions
def get_suggestions(missing):
    return ["Learn " + skill for skill in missing]


# 🔹 Job match %
def calculate_job_match(clean_text_data, job_desc):
    resume_words = set(clean_text_data.split())
    job_words = set(job_desc.lower().split()) if job_desc else set()

    if len(job_words) == 0:
        return 0

    match = resume_words.intersection(job_words)
    return (len(match) / len(job_words)) * 100


# ============================================================
# 🔥 NEW FEATURES START HERE
# ============================================================

# 🔹 1. Score Breakdown

def score_breakdown(found_skills, missing_skills, total, clean_text_data):
    # Skills weight = 70%
    skills_score = (len(found_skills) / total) * 70 if total > 0 else 0

    # Experience weight = 20%
    exp_score = 20 if "experience" in clean_text_data.lower() else 0

    # Education weight = 10%
    edu_score = 10 if "education" in clean_text_data.lower() else 0

    final_score = skills_score + exp_score + edu_score
    if final_score > 100:
        final_score = 100

    return {
        "total": total,
        "skills": round(skills_score, 2),
        "experience": exp_score,
        "education": edu_score,
        "final_score": round(final_score, 2),
    }




def improvement_tips(missing_skills, job_desc):

    tips = []

    # ✅ Skill-based recommendations
    skill_resources = {

        "python": "Learn Python from CodeWithHarry and practice OOP concepts.",

        "django": "Build Django projects and learn authentication & CRUD.",

        "flask": "Learn Flask APIs and mini projects from TechGun or CodeWithHarry.",

        "sql": "Practice SQL queries on LeetCode and HackerRank.",

        "react": "Build React projects and learn hooks and APIs.",

        "javascript": "Practice ES6, DOM manipulation, and async JS.",

        "mongodb": "Learn MongoDB CRUD operations and aggregation pipeline.",

        "node": "Build backend APIs using Node.js and Express.",

        "express": "Practice REST APIs using Express.js.",

        "powerbi": "Create Power BI dashboards and visualization projects.",

        "pandas": "Practice data analysis and cleaning using Pandas.",

        "numpy": "Learn arrays and mathematical operations in NumPy.",

        "tableau": "Learn Tableau dashboards and data visualization projects from YouTube and practice on Kaggle."

        # "rest api":"Practice REST API development using Flask or FastAPI and learn GET, POST, PUT, DELETE methods.",
        
        # "fastapi":"Learn FastAPI and build high-performance REST APIs with Python."
    }

    # ✅ Missing skills recommendation
    for skill in missing_skills:

        if skill in skill_resources:

            tips.append(skill_resources[skill])

        else:

            tips.append(f"Improve your {skill} skill.")

    # ✅ Job description based tips
    if "project" in job_desc.lower():

        tips.append("Mention relevant projects in your resume.")

    if "team" in job_desc.lower():

        tips.append("Highlight teamwork or collaboration experience.")

    return tips
# 🔹 3. Job Recommendations
def job_recommendations(found_skills, role):

    # ✅ Role Based Recommendations

    role_jobs = {

        "Data Analyst": [
            "Data Analyst",
            "Business Analyst",
            "Data Visualization Analyst"
        ],

        "Python Developer": [
            "Python Developer",
            "Django Web Developer",
            "Backend Developer"
        ],

        "Mern Stack Developer": [
            "Mern Stack Developer",
            "React Developer",
            "Full Stack Developer"
        ],

        "Frontend Developer": [
            "Frontend Developer",
            "React Developer",
            "UI Developer"
        ],

        "Backend Developer": [
            "Backend Developer",
            "API Developer",
            "Node.js Developer"
        ],

        "Full Stack Developer": [
            "Full Stack Developer",
            "Software Engineer",
            "Web Developer"
        ],

        "ML Engineer": [
            "ML Engineer",
            "AI Engineer",
            "Data Scientist"
        ]
    }

    # ✅ Return role-based jobs
    if role in role_jobs:

        return role_jobs[role]

    # ✅ fallback
    return ["General IT Role"]
#AI suggestion
def ai_suggestions(clean_text, missing_skills, score, role):
    suggestions = []
    text = clean_text.lower()

    # 🔹 Score-based suggestion
    if score < 40:
        suggestions.append("Your resume ATS score is low. Add relevant keywords and improve formatting.")
    elif score < 70:
        suggestions.append(f"Your resume is good, but you can improve it further for the {role} role.")
    else:
        suggestions.append(f"Excellent resume! Focus on advanced skills for {role} role.")

    # 🔹 Skill-based suggestions (SMART)
    for skill in missing_skills[:3]:
        suggestions.append(f"Add '{skill}' skill for {role} role to improve job match.")

    # 🔹 Action verbs check
    action_words = ["developed", "built", "designed", "implemented"]
    if not any(word in text for word in action_words):
        suggestions.append("Use action verbs like Developed, Built, Designed to improve impact.")

    # 🔹 Project section
    if "project" not in text:
        suggestions.append("Add a project section to showcase practical experience.")

    # 🔹 Summary section
    if "summary" not in text and "objective" not in text:
        suggestions.append("Add a strong professional summary at the top of your resume.")

    # 🔹 Measurable achievements
    if "%" not in text:
        suggestions.append("Include measurable achievements (e.g., increased efficiency by 20%).")

    # 🔹 Role-specific suggestion (🔥 important)
    if role == "Data Analyst" and "powerbi" not in text:
        suggestions.append("Add Power BI or Tableau projects for Data Analyst roles.")

    if role == "Python Developer" and not any(x in text for x in ["django", "flask"]):
        suggestions.append("Add Django or Flask framework experience to strengthen your profile.")

    return suggestions





