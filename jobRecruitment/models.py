from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="company_profile"
    )
    

    def __str__(self):
        return f"{self.name} - {self.industry}"
    
class Candidate(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    job = models.CharField(max_length=100, default='Not Specified')
    resume = models.TextField(default='No Resume Provided')
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="candidate_profile"
    )
    

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class JobPosting(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)
    posted_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.company.name}"
    
from django.db import models

class Interview(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = 'scheduled', 'Scheduled'
        COMPLETED = 'completed', 'Completed'
        PASSED = 'passed', 'Passed'
        REJECTED = 'rejected', 'Rejected'
        CANCELLED = 'cancelled', 'Cancelled'

    candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE, related_name='interviews')
    job = models.ForeignKey('JobPosting', on_delete=models.CASCADE, related_name='interviews')
    company = models.ForeignKey('Company',on_delete=models.CASCADE,related_name='interviews',null=True,blank=True)

    interviewer = models.CharField(max_length=100)
    interview_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-interview_time']

    def __str__(self):
        return f"{self.candidate} | {self.job} | {self.interview_time:%Y-%m-%d %H:%M}"
