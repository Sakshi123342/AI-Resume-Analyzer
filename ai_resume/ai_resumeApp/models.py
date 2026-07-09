from django.db import models


class ResumeData(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    resume = models.FileField(upload_to="resumes/")
    job_desc = models.TextField()
    ats_score = models.FloatField()
    job_match = models.FloatField()
    skills_found = models.TextField(blank=True)   # role-specific
    missing = models.TextField(blank=True)
    job_recommendation = models.TextField(blank=True)
    
    # ✅ Add this new field
    general_skills = models.TextField(blank=True)  