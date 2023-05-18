from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator

from .forms import (
    LoginForm,
    UserRegistrationForm,
    UserProfileForm,
    UserPictureForm
)
from .decorators import not_login_required
from .models import User, Follow
from blog.views import Blog

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

def user_profile(request):
    account = get_object_or_404(User, pk=request.user.pk)
    form = UserProfileForm(instance=account)

    if request.method == "POST":
        if request.user.pk != account.pk:
            return redirect('home')
        form = UserProfileForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated sucessfully!")
            return redirect('profile')
        else:
            print(form.errors)

    context = {
        "account": account,
        "form": form
    }
    return render(request, 'user-profile.html', context)

def user_picture(request):
    if request.method == "POST":
        form = UserPictureForm(request.POST, request.FILES)
        if form.is_valid():
            image = request.FILES['profile_image']
            user = get_object_or_404(User, pk=request.user.pk)
            if request.user.pk != user.pk:
                return redirect('home')

            user.image = image
            user.save()
            messages.success(request, "Profile picture updated successfully!")
        else:
            print(form.errors)
    return redirect('user_profile')

def user_blogs(request):
    queryset = request.user.user_blogs.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 6)
    delete = request.GET.get('delete', None)

    if delete:
        blog = get_object_or_404(Blog, pk=delete) 
        if request.user.pk != blog.user.pk:
            return redirect('home')
        blog.delete()
        messages.success(request, "Your blog has been deleted!")
        return redirect('my_blogs')

    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')

    context = {
        "blogs": blogs,
        "paginator": paginator
    }   
    return render(request, 'user-blogs.html', context) 

def user_info(request, username):
    account = get_object_or_404(User, username=username)
    following = False
    muted = None

    if request.user.is_authenticated:
        if request.user.id == account.id:
            return redirect("user_profile")

        followers = account.followers.filter(
            followed_by__id=request.user.id
        )
        if followers.exists():
            following = True

    if following:
        queryset = followers.first()
        if queryset.muted:
            muted = True
        else:
            muted = False

    context = {
        "account": account,
        "following": following,
        "muted": muted
    }
    return render(request, 'user-info.html', context)


def user_follow_or_unfollow(request, id):
    followed = get_object_or_404(User, id=id)
    followed_by = get_object_or_404(User, id=request.user.id)

    follow, created = Follow.objects.get_or_create(
        followed=followed,
        followed_by=followed_by
    )

    if created:
        followed.followers.add(follow)
    else:
        followed.followers.remove(follow)
        follow.delete()
    return redirect('user_info', username=followed.username)

def user_mute_or_unmute(request, id):
    user = get_object_or_404(User, pk=id)
    follower = get_object_or_404(User, pk=request.user.pk)
    instance = get_object_or_404(
        Follow,
        followed=user,
        followed_by=follower
    )

    if instance.muted:
        instance.muted = False
        instance.save()
    else:
        instance.muted = True
        instance.save()
    return redirect('user_info', username=user.username)