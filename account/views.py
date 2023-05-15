from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.cache import never_cache
from django.contrib import messages

from .forms import (
    LoginForm,
    UserRegistrationForm
)
from .decorators import not_login_required

@never_cache
@not_login_required
def user_registration(request):
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            messages.success(request, 'Registration successful!')
            return redirect('user_login')
        
    context = {
        'form' : form
    }
    return render(request, 'registration.html', context)

@never_cache
@not_login_required
def user_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password = form.cleaned_data.get('password')
            )
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.warning(request, 'wrong creadentials')
    context = {
        'form' : form
    }
    return render(request, 'login.html', context)

def user_logout(request):
    logout(request)
    return redirect('user_login')