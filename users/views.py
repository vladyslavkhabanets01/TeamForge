from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm, UserProfileForm
from .models import UserProfile


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Вітаємо, {user.username}! Ваш акаунт створено.')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, 'Невірний нікнейм або пароль.')
    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_profile, _ = UserProfile.objects.get_or_create(user=user)
    posts = user.posts.all()[:5]
    lfg_posts = user.lfg_posts.filter(is_active=True)[:3]
    return render(request, 'users/profile.html', {
        'profile_user': user,
        'user_profile': user_profile,
        'posts': posts,
        'lfg_posts': lfg_posts,
    })


@login_required
def edit_profile(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профіль оновлено.')
            return redirect('users:profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'users/edit_profile.html', {'form': form})
