# scheduling/views_api.py (or your_app/views_api.py)

from datetime import timedelta
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Candidate, JobPosting, Company, Interview
from .serializers import (
    CandidateSerializer,
    JobPostingSerializer,
    CompanySerializer,
    InterviewSerializer
)


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


class JobPostingViewSet(viewsets.ModelViewSet):
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class InterviewViewSet(viewsets.ModelViewSet):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        candidate = serializer.validated_data['candidate']
        job = serializer.validated_data['job']
        interview_time = serializer.validated_data['interview_time']

        # Check overlapping interviews (same candidate + near time)
        clash = Interview.objects.filter(
            candidate=candidate,
            interview_time__lte=interview_time + timedelta(minutes=29),
            interview_time__gte=interview_time - timedelta(minutes=29)
        ).exists()

        if clash:
            return Response(
                {'detail': "This candidate already has an interview near this time."},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
