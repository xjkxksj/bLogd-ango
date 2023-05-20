from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('frontpage')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            error_message = 'Invalid registration data'
    else:
        form = UserRegistrationForm()
        error_message = None

    return render(request, 'register.html', {'form': form, 'error_message': error_message})


@login_required
def frontpage_view(request):
    is_user_logged_in = request.user.is_authenticated
    context = {
        'is_user_logged_in': is_user_logged_in,
    }
    return render(request, 'frontpage.html', context)

@login_required
def account_view(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'account.html', context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('frontpage')

def authors_view(request):
    return render(request, 'authors.html')

def favourites_view(request):
    return render(request, 'favourites.html')
