from django.contrib import admin
from .models import ResumeData
from django.utils.html import format_html

@admin.register(ResumeData)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'resume_link','ats_score','job_match']

    def resume_link(self, obj):
        if obj.resume:
            return format_html("<a href='{}' target='_blank'>Download</a>", obj.resume.url)
        return "No file"

    resume_link.short_description = "Resume"
