from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import CandidateForm, CompanyForm, JobPostingForm, InterviewForm
from .models import Candidate, Company, JobPosting, Interview
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, PermissionRequiredMixin



def home(request):
    context = {
        'company_count': Company.objects.count(),
        'candidate_count': Candidate.objects.count(),
        'job_posting_count': JobPosting.objects.count(),
        'interview_count': Interview.objects.count(),
    }
    return render(request, 'home.html', context)


@login_required
@permission_required('jobRecruitment.view_company', raise_exception=True)
def companies_list(request):
    companies = Company.objects.all()
    return render(request, 'company/companies.html', {'companies': companies})

@login_required
@permission_required('jobRecruitment.view_candidate', raise_exception=True)
def candidates_list(request):
    user = request.user

    # Check if user is a Candidate
    if user.groups.filter(name__iexact='Candidates').exists():
        try:
            candidate_profile = Candidate.objects.get(user=user)
            candidates = Candidate.objects.filter(id=candidate_profile.id)
        except Candidate.DoesNotExist:
            candidates = Candidate.objects.none()
    else:   
        # All other users (Company, Admin) see all candidates
        candidates = Candidate.objects.all()

    return render(request, 'candidate/candidates.html', {'candidates': candidates})

@login_required
@permission_required('jobRecruitment.view_jobposting', raise_exception=True)
def job_postings_list(request):
    user = request.user

    # Check if user is a Company
    if user.groups.filter(name__iexact='Companies').exists():
        try:
            company_profile = Company.objects.get(user=user)
            job_postings = JobPosting.objects.filter(company=company_profile).order_by('-posted_date')
        except Company.DoesNotExist:
            job_postings = JobPosting.objects.none()
    else:   
        # All other users see all job postings
        job_postings = JobPosting.objects.all().order_by('-posted_date')

    return render(request, 'job_posting/job_postings.html', {'job_postings': job_postings})

@login_required
@permission_required('jobRecruitment.view_candidate', raise_exception=True)
def view_candidate_resume(request, id):
    candidate = get_object_or_404(Candidate, id=id)
    return render(request, 'candidate/view_resume.html', {'candidate': candidate})

# CREATE CANDIDATE
@login_required
@permission_required('jobRecruitment.add_candidate', raise_exception=True)
def create_candidate(request):
    if request.method == "POST":
        form = CandidateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Candidate created successfully!')
            return redirect('candidates')
    else:
        form = CandidateForm()
    return render(request, 'candidate/create_candidate.html', {'form': form})

# UPDATE CANDIDATE
@login_required
@permission_required('jobRecruitment.change_candidate', raise_exception=True)
def update_candidate(request, id):
    candidate = get_object_or_404(Candidate, id=id)
    form = CandidateForm(request.POST or None, instance=candidate)
    if form.is_valid():
        form.save()
        messages.success(request, 'Candidate updated successfully!')
        return redirect('candidates')
    return render(request, 'candidate/update_candidate.html', {'form': form})

# DELETE CANDIDATE
@login_required
@permission_required('jobRecruitment.delete_candidate', raise_exception=True)
def delete_candidate(request, id):
    candidate = get_object_or_404(Candidate, id=id)
    if request.method == "POST":
        candidate.delete()
        messages.success(request, 'Candidate deleted successfully!')
        return redirect('candidates')
    return render(request, 'candidate/delete_candidate.html', {'candidate': candidate})

# CREATE COMPANY
@login_required
@permission_required('jobRecruitment.add_company', raise_exception=True)
def create_company(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company created successfully!')
            return redirect('companies')
    else:
        form = CompanyForm()
    return render(request, 'company/create_company.html', {'form': form})

# UPDATE COMPANY
@login_required
@permission_required('jobRecruitment.change_company', raise_exception=True)
def update_company(request, id):
    company = get_object_or_404(Company, id=id)
    form = CompanyForm(request.POST or None, instance=company)
    if form.is_valid():
        form.save()
        messages.success(request, 'Company updated successfully!')
        return redirect('companies')
    return render(request, 'company/update_company.html', {'form': form})

# DELETE COMPANY
@login_required
@permission_required('jobRecruitment.delete_company', raise_exception=True)
def delete_company(request, id):
    company = get_object_or_404(Company, id=id)
    if request.method == "POST":
        company.delete()
        messages.success(request, 'Company deleted successfully!')
        return redirect('companies')
    return render(request, 'company/delete_company.html', {'company': company})

# CREATE JOB POSTING
@login_required
@permission_required('jobRecruitment.add_jobposting', raise_exception=True)
def create_job_posting(request):
    if request.method == "POST":
        form = JobPostingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job posting created successfully!')
            return redirect('job_postings')
    else:
        form = JobPostingForm()
    return render(request, 'job_posting/create_job_posting.html', {'form': form})

# UPDATE JOB POSTING
@login_required
@permission_required('jobRecruitment.change_jobposting', raise_exception=True)
def update_job_posting(request, id):
    job_posting = get_object_or_404(JobPosting, id=id)
    form = JobPostingForm(request.POST or None, instance=job_posting)
    if form.is_valid():
        form.save()
        messages.success(request, 'Job posting updated successfully!')
        return redirect('job_postings')
    return render(request, 'job_posting/update_job_posting.html', {'form': form})

# DELETE JOB POSTING
@login_required
@permission_required('jobRecruitment.delete_jobposting', raise_exception=True)
def delete_job_posting(request, id):
    job_posting = get_object_or_404(JobPosting, id=id)
    if request.method == "POST":
        job_posting.delete()
        messages.success(request, 'Job posting deleted successfully!')
        return redirect('job_postings')
    return render(request, 'job_posting/delete_job_posting.html', {'job_posting': job_posting})


class InterviewListView(PermissionRequiredMixin, ListView):
    permission_required = 'jobRecruitment.view_interview'
    model = Interview
    template_name = 'interview/interviews.html'
    context_object_name = 'interviews'


from django.utils import timezone

class InterviewCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'jobRecruitment.add_interview'
    model = Interview
    form_class = InterviewForm
    template_name = 'interview/create_interview.html'
    success_url = reverse_lazy('interviews')
    
    def form_valid(self, form):
        from django.utils import timezone
        interview = form.save(commit=False)
        
        try:
            company = Company.objects.get(user=self.request.user)
            interview.company = company
        except Company.DoesNotExist:
            messages.error(self.request, "You don't have a company profile.")
            return self.form_invalid(form)
        
        # Get interview details
        candidate = interview.candidate
        interview_time = interview.interview_time
        
        # Check if candidate has overlapping interviews (within 1 hour window)
        candidate_conflict = Interview.objects.filter(
            candidate=candidate,
            interview_time__lte=interview_time + timezone.timedelta(minutes=59),
            interview_time__gte=interview_time - timezone.timedelta(minutes=59)
        ).exists()
        
        if candidate_conflict:
            messages.warning(
                self.request, 
                f"Candidate {candidate.first_name} {candidate.last_name} already has an interview scheduled around {interview_time:%Y-%m-%d %H:%M}."
            )
            return self.form_invalid(form)
        
        # Check if company has overlapping interviews for the same job (within 1 hour window)
        company_conflict = Interview.objects.filter(
            company=company,
            job=interview.job,
            interview_time__lte=interview_time + timezone.timedelta(minutes=59),
            interview_time__gte=interview_time - timezone.timedelta(minutes=59)
        ).exists()
        
        if company_conflict:
            messages.warning(
                self.request,
                f"You already have an interview scheduled for {interview.job.title} around {interview_time:%Y-%m-%d %H:%M}."
            )
            return self.form_invalid(form)
        
        return super().form_valid(form)

class InterviewUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'jobRecruitment.change_interview'
    model = Interview
    form_class = InterviewForm
    template_name = 'interview/update_interview.html'
    success_url = reverse_lazy('interviews')


class InterviewDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'jobRecruitment.delete_interview'
    model = Interview
    template_name = 'interview/delete_interview.html'
    success_url = reverse_lazy('interviews')


def custom_permission_denied_view(request, exception=None):
    return render(request, "403.html", status=403)

# INTERVIEWS LIST
# INTERVIEWS LIST
@login_required
@permission_required('jobRecruitment.view_interview', raise_exception=True)
def interviews_list(request):
    user = request.user

    # Check if user is a Company
    if user.groups.filter(name__iexact='Companies').exists():
        try:
            company_profile = Company.objects.get(user=user)
            interviews = Interview.objects.filter(
                company=company_profile
            ).select_related('candidate', 'job', 'company').order_by('-interview_time')
        except Company.DoesNotExist:
            interviews = Interview.objects.none()
    
    # Check if user is a Candidate
    elif user.groups.filter(name__iexact='Candidates').exists():
        try:
            candidate_profile = Candidate.objects.get(user=user)
            interviews = Interview.objects.filter(
                candidate=candidate_profile
            ).select_related('company', 'job', 'candidate').order_by('-interview_time')
        except Candidate.DoesNotExist:
            interviews = Interview.objects.none()

    # Admin or other users see all interviews
    else:
        interviews = Interview.objects.select_related(
            'candidate', 'company', 'job'
        ).all().order_by('-interview_time')

    return render(request, 'interview/interviews.html', {'interviews': interviews})



@permission_required('jobRecruitment.add_interview', raise_exception=True)
def create_interview(request):
    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            
            try:
                company = Company.objects.get(user=request.user)
                interview.company = company
                interview.save()
                messages.success(request, "Interview created successfully.")
                return redirect('interviews')
            except Company.DoesNotExist:
                messages.error(request, "You don't have a company profile.")
                return redirect('interviews')
    else:
        form = InterviewForm()

    return render(request, 'interview/create_interview.html', {'form': form})