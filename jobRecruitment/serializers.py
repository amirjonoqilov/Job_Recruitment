from rest_framework import serializers
from .models import Candidate, Company, JobPosting, Interview


# ---- Candidate ----
class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'


# ---- Company ----
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


# ---- Job Posting ----
class JobPostingSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = JobPosting
        fields = '__all__'


# ---- Interview ----
class InterviewSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(source='candidate.user.get_full_name', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = Interview
        fields = '__all__'
