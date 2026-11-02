import re
import pdfplumber
from django.shortcuts import render, get_object_or_404
from .models import ResumeData
from rapidfuzz import fuzz
from .utils import score_breakdown, improvement_tips, job_recommendations
from .utils import detect_role_from_jd
from .utils import detect_role
from .utils import clean_text
from.utils import match_keywords
import traceback
# ✅ Extract text from PDF
def extract_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
    return text.lower()

# ✅ Role-wise keywords dictionary
from fuzzywuzzy import fuzz


role_keywords = {
    "Python Developer": ["python", "django", "flask", "sql"],
    
    "Mern Stack Developer": [

    "react",

    "node",

    "express",

    "mongodb",

    "javascript"
],
    "Data Analyst": ["excel", "tableau", "power bi", "python", "sql","numpy","pandas"],
    "Java Developer": ["java", "spring", "hibernate", "mysql"],
    "Android Developer": ["java", "kotlin", "android", "xml"],
    "Frontend Developer": ["html", "css", "javascript", "react"],
    "Backend Developer": ["node", "express", "django", "flask"],
    "Full Stack Developer": ["javascript", "react", "node", "django", "flask", "sql", "mongodb"]
}

def detect_role_from_jd(job_desc):

    # 🔥 normalize text
    job_desc = job_desc.lower()
    job_desc = job_desc.replace(".", " ")
    job_desc = job_desc.replace("-", " ")
    job_desc = job_desc.replace(",", " ")
    job_desc = job_desc.replace("/", " ")
    roles = {

        "Python Developer": [
            "python", "django", "flask", "sql"
        ],

         "Mern Stack Developer": [
           "mern",
           "mern stack",
           "mernstack",
           "react",
           "react js",
           "reactjs",
           "node",
           "node js",
           "nodejs",
           "express",
           "express js",
           "expressjs",
           "mongodb",
           "mongo"
    ],
        "Data Analyst": [
            "data analyst",
            "analytics",
            "data analytics",
            "data analysis",
            "excel",
            "tableau",
            "power bi",
            "sql"
        ],

        "Java Developer": [
            "java",
            "spring",
            "hibernate",
            "mysql"
        ],

        "Android Developer": [
            "android",
            "kotlin",
            "xml"
        ],

        "Full Stack Developer": [
            "full stack",
            "fullstack",
            "frontend",
            "backend",
            "react",
            "node",
            "django",
            "flask",
            "mongodb"
        ],

        "Frontend Developer": [
            "frontend",
            "html",
            "css",
            "javascript",
            "react"
        ],

        "Backend Developer": [
            "backend",
            "django",
            "flask",
            "node",
            "express"
        ],

        "ML Engineer": [
            "machine learning",
            "deep learning",
            "tensorflow",
            "pandas",
            "numpy",
            "scikit learn"
        ]
    }

    best_role = "General Role"
    max_score = 0

    # 🔥 keyword matching
    for role, keywords in roles.items():

        score = 0

        for word in keywords:
            if word in job_desc:
                score += 1

        print(role, score)   # 🔍 debug
        if role == "Mern Stack Developer" and score >= 2:
         return "Mern Stack Developer"
        # highest score role select
        if score > max_score:
            max_score = score
            best_role = role

    return best_role

def detect_skills(text, role):
    text_lower = text.lower()
    found = []
    missing = []

    for skill in role_keywords.get(role, []):
        score = fuzz.partial_ratio(skill, text_lower)
        if score >= 70:
            found.append((skill, score))
        else:
            missing.append((skill, score))

    return found, missing
 

def calculate_job_match(resume_text, job_desc):
    if not job_desc:
        return 0

    resume_text = resume_text.lower()
    job_desc = job_desc.lower()

    resume_words = set(re.findall(r'\w+', resume_text))
    job_words = set(re.findall(r'\w+', job_desc))

    common = resume_words.intersection(job_words)

    if len(job_words) == 0:
        return 0
    return (len(common) / len(job_words)) * 100


# ✅ Home view
# 
def home(request):
    if request.method != 'POST':
        return render(request, 'home.html')

    try:
        print("STEP 1: Resume processing started", flush=True)

        resume = request.FILES.get('resume')

        if not resume:
            return render(request, 'home.html', {
                'error': 'Please upload resume'
            })

        if not resume.name.lower().endswith('.pdf'):
            return render(request, 'home.html', {
                'error': 'Only PDF allowed'
            })

        # Extract text from PDF
        print("STEP 2: Extracting PDF text", flush=True)

        text = extract_text(resume)
        clean_text_data = clean_text(text)

        job_desc = request.POST.get('job_desc', "")

        # Auto detect role
        print("STEP 3: Detecting role", flush=True)

        role = detect_role_from_jd(job_desc)

        print("Detected Role:", role, flush=True)

        # Match keywords
        print("STEP 4: Matching skills", flush=True)

        found_skills, missing_skills = match_keywords(text, role)

        print("Found Skills:", found_skills, flush=True)
        print("Missing Skills:", missing_skills, flush=True)

        # Calculate total skills
        total_skills = len(role_keywords.get(role, []))

        if role == "Mern Stack Developer":
            total_skills = 5

        # Calculate ATS score
        print("STEP 5: Calculating ATS score", flush=True)

        breakdown = score_breakdown(
            found_skills,
            missing_skills,
            total_skills,
            text
        )

        ats_score = breakdown["final_score"]

        print("ATS Score:", ats_score, flush=True)

        # Improvement tips
        print("STEP 6: Generating tips and jobs", flush=True)

        tips = improvement_tips(missing_skills, job_desc)

        jobs = job_recommendations(found_skills, role)

        match_score = calculate_job_match(text, job_desc)

        # AI suggestions
        print("STEP 7: Generating AI suggestions", flush=True)

        from .utils import ai_suggestions

        suggestions = ai_suggestions(
            text,
            missing_skills,
            ats_score,
            role
        )

        # Save data in session
        print("STEP 8: Saving session data", flush=True)

        request.session["breakdown"] = breakdown
        request.session["tips"] = tips
        request.session["jobs"] = jobs
        request.session["found_skills"] = found_skills
        request.session["missing_skills"] = missing_skills

        if role == "Mern Stack Developer":
            request.session["total_skills"] = [
                "react",
                "node",
                "express",
                "mongodb",
                "javascript"
            ]
        else:
            request.session["total_skills"] = role_keywords.get(role, [])

        # Save resume in database
        print("STEP 9: Saving resume in database", flush=True)

        ResumeData.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            resume=resume,
            job_desc=job_desc,
            ats_score=ats_score,
            job_match=match_score,
            skills_found=", ".join(found_skills),
            missing=", ".join(missing_skills),
            job_recommendation=", ".join(suggestions)
        )

        # Open result page
        print("STEP 10: Opening result page", flush=True)

        return render(request, 'result.html', {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'role': role,
            'score': round(ats_score, 2),
            'job_match': round(match_score, 2),
            'found_skills': found_skills,
            'missing_skills': missing_skills,
            'suggestions': suggestions,
        })

    except Exception as e:
        print("HOME VIEW ERROR:", repr(e), flush=True)
        traceback.print_exc()

        return render(request, 'home.html', {
            'error': 'Resume analysis failed. Please try again.'
        })


# ✅ Scores view
def scores(request):

    context = {

        "breakdown": request.session.get("breakdown", {}),

        "tips": request.session.get("tips", []),

        "jobs": request.session.get("jobs", []),

        "total_skills": request.session.get("total_skills", []),

        "missing_skills": request.session.get("missing_skills", []),
    }

    return render(request, "scores.html", context)

# ✅ Dashboard view
def dashboard(request):
    breakdown = request.session.get("breakdown", {})
    context = {
        # yahan final_score use karo, total nahi
        'score': breakdown.get("final_score", 0),
        'breakdown': breakdown,
        'tips': request.session.get("tips", []),
        'jobs': request.session.get("jobs", []),
        'found_skills': request.session.get("found_skills", []),
        'missing_skills': request.session.get("missing_skills", [])
    }
    return render(request, 'dashboard.html', context)
from .utils import score_breakdown, improvement_tips, job_recommendations

# def resume_list(request):
#     resumes = ResumeData.objects.values("id", "name")
#     return render(request, "resume_list.html", {"resumes": resumes})

# def resume_detail(request, resume_id):
#     resume = get_object_or_404(ResumeData, id=resume_id)
#     return render(request, "resume_detail.html", {"resume": resume})



