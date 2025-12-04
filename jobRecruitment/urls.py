from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

from .views import (
    InterviewListView,
    InterviewCreateView,
    InterviewUpdateView,
    InterviewDeleteView
)

from .views_api import (
    CandidateViewSet,
    JobPostingViewSet,
    CompanyViewSet,
    InterviewViewSet
)

router = DefaultRouter()
router.register(r'candidates', CandidateViewSet)
router.register(r'jobs', JobPostingViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'interviews', InterviewViewSet)

urlpatterns = [
    path('api/', include(router.urls)),

    path('', views.home, name='home'),
    path('companies/', views.companies_list, name='companies'),
    path('candidates/', views.candidates_list, name='candidates'),

        # Candidate URLs
    path('candidates/create/', views.create_candidate, name='create_candidate'),
    path('candidates/update/<int:id>/', views.update_candidate, name='update_candidate'),
    path('candidates/delete/<int:id>/', views.delete_candidate, name='delete_candidate'),

    path('candidate/<int:id>/resume/', views.view_candidate_resume, name='view_candidate_resume'),
    
    # Company URLs
    path('companies/create/', views.create_company, name='create_company'),
    path('companies/update/<int:id>/', views.update_company, name='update_company'),
    path('companies/delete/<int:id>/', views.delete_company, name='delete_company'),

    path('job-postings/', views.job_postings_list, name='job_postings'),
    path('job-postings/create/', views.create_job_posting, name='create_job_posting'),
    path('job-postings/update/<int:id>/', views.update_job_posting, name='update_job_posting'),
    path('job-postings/delete/<int:id>/', views.delete_job_posting, name='delete_job_posting'),

    path('interviews/', views.interviews_list, name='interviews'),
    path('interviews/create/', InterviewCreateView.as_view(), name='create_interview'),
    path('interviews/update/<int:pk>/', InterviewUpdateView.as_view(), name='update_interview'),
    path('interviews/delete/<int:pk>/', InterviewDeleteView.as_view(), name='delete_interview'),

]

handler403 = "jobRecruitment.views.custom_permission_denied_view"