import os
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm, NewPostForm
from .models import UserProfile, Post, Tag
from django.utils import timezone
from PIL import Image
from django.core.files import File
from django.conf import settings
from django.core.paginator import Paginator

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
    registration_date = request.user.date_joined
    registration_date = timezone.localtime(registration_date)
    context = {
        'user_profile': user_profile,
        'registration_date': registration_date,
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
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            image_file = request.FILES.get('image')
            if image_file:
                image = Image.open(image_file)
                desired_size = (400, 400)
                image.thumbnail(desired_size)
                image_filename = image_file.name
                image_extension = image_filename.split('.')[-1]
                temp_image_path = os.path.join(settings.MEDIA_ROOT, 'post_images', f'temp_image.{image_extension}')
                image.save(temp_image_path)
                with open(temp_image_path, 'rb') as f:
                    post.image.save(image_filename, File(f), save=True)

                os.remove(temp_image_path)
            else:
                no_image_path = os.path.join(settings.MEDIA_ROOT, 'post_images', 'noimage.jpg')
                with open(no_image_path, 'rb') as f:
                    post.image.save('noimage.jpg', File(f), save=True)

            form.save_m2m()

            return redirect('latestposts')
    else:
        form = NewPostForm()

    tags = Tag.objects.all()

    return render(request, 'newpost.html', {'form': form, 'tags': tags})

def tag_posts_view(request, tag_name):
    tag = Tag.objects.get(name=tag_name)
    posts = tag.post_set.all().order_by('-post_added_date')
    context = {
        'posts': posts,
        'tag': tag.name,
    }
    return render(request, 'tag_posts.html', context)

def authors_view(request):
    return render(request, 'authors.html')

def favourites_view(request):
    return render(request, 'favourites.html')

def latestposts_view(request):
    all_posts = Post.objects.order_by('-post_added_date')
    paginator = Paginator(all_posts, 9)
    page_number = request.GET.get('page')
    latest_posts = paginator.get_page(page_number)
    context = {'latestposts': latest_posts}
    return render(request, 'latestposts.html', context)

def post_view(request, post_id):
    post = Post.objects.get(id=post_id)
    context = {'post': post}
    return render(request, 'post.html', context)
