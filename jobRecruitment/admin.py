from django.contrib import admin
from .models import Company, Candidate, JobPosting, Interview

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'job', 'interviewer', 'interview_time', 'status')
    search_fields = ('candidate__first_name', 'candidate__last_name', 'job__title', 'interviewer')
    list_filter = ('status', 'job', 'interview_time')
    ordering = ('-interview_time',)

class InterviewInline(admin.TabularInline):
    model = Interview
    extra = 1
    fields = ('job', 'interviewer', 'interview_time', 'status')

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'job')
    search_fields = ('first_name', 'last_name', 'email', 'job')
    list_filter = ('job',)
    inlines = [InterviewInline]

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'location', 'email')
    search_fields = ('name', 'industry', 'location')
    list_filter = ('industry', 'location')

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'salary', 'posted_date')
    search_fields = ('title', 'company__name', 'location')
    list_filter = ('company', 'location', 'posted_date')
    ordering = ('-posted_date',)
    inlines = [InterviewInline]