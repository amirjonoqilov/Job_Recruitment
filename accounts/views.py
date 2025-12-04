from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.urls import reverse

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

    form = UserCreationForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save()
        messages.success(request, "Registration successful. You can now log in.")

        return redirect('login')  # redirect to login after registration

    return render(request, 'accounts/register.html', {'form': form})
