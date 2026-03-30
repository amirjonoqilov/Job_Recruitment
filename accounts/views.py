from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.urls import reverse
from .forms import CustomUserCreationForm
from jobRecruitment.models import Candidate, Company
from django.contrib.auth.models import Group

# LOGIN VIEW
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # or your dashboard page

    form = AuthenticationForm(request, data=request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, "You are now logged in.")

        # Redirect to 'next' if available, otherwise go to home/dashboard
        next_url = request.GET.get('next') or reverse('home')
        return redirect(next_url)

    return render(request, 'accounts/login.html', {'form': form})

# LOGOUT VIEW
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')  # redirect to login page after logout
    

# REGISTER VIEW
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # or your dashboard page

    form = CustomUserCreationForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save()
        role = form.cleaned_data['role']
        
        if role == 'candidate':
            Candidate.objects.create(
                user=user,
                first_name=user.username,  # placeholder
                last_name='',
                email=user.email or '',
                phone_number='',
                job='Not Specified',
                resume='No Resume Provided'
            )
            group, created = Group.objects.get_or_create(name='Candidates')
            user.groups.add(group)
        elif role == 'company':
            Company.objects.create(
                user=user,
                name=user.username,  # placeholder
                location='',
                industry='',
                email=user.email or ''
            )
            group, created = Group.objects.get_or_create(name='Companies')
            user.groups.add(group)
        
        messages.success(request, "Registration successful. You can now log in.")

        return redirect('login')  # redirect to login after registration

    return render(request, 'accounts/register.html', {'form': form})
