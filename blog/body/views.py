from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm, NewPostForm
from .models import UserProfile, Post

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, nickname=form.cleaned_data['nickname'])
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
        else:
            error_message = 'Invalid registration data'
            return render(request, 'register.html', {'form': form, 'error_message': error_message})
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have been successfully logged in.')
                return redirect('frontpage')
        messages.error(request, 'Invalid username or password')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def account_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = {
        'user_profile': user_profile,
    }
    return render(request, 'account.html', context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('frontpage')

def frontpage_view(request):
    is_user_logged_in = request.user.is_authenticated
    context = {
        'is_user_logged_in': is_user_logged_in,
    }
    return render(request, 'frontpage.html', context)

@login_required
def newpost_view(request):
    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():

            return redirect('frontpage') 
    else:
        form = NewPostForm()
    
    context = {'form': form}
    return render(request, 'newpost.html', context)

def authors_view(request):
    return render(request, 'authors.html')

def favourites_view(request):
    return render(request, 'favourites.html')
