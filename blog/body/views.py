from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, UserLoginForm, NewPostForm, CommentForm
from .models import UserProfile, Post, Tag, Comment
from django.urls import reverse
from django.utils import timezone
from django.core.paginator import Paginator
from django.utils.text import slugify

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
            post.slug = slugify(post.title)

            image_file = request.FILES.get('image')
            if image_file:
                post.image = image_file

            post.save()
            form.save_m2m()

            return redirect('latestposts')
    else:
        form = NewPostForm()

    tags = Tag.objects.all()

    return render(request, 'newpost.html', {'form': form, 'tags': tags})

def tag_posts_view(request, tag_name):
    tag = Tag.objects.get(name=tag_name)
    posts = tag.post_set.all().order_by('-post_added_date')
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'tag': tag.name,
        'posts': page_obj,
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

def post_view(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST' and request.user.is_authenticated:
        content = request.POST.get('content')
        nickname = request.user.userprofile.nickname
        comment = Comment(post=post, content=content, nickname=nickname)
        comment.save()

    context = {'post': post}
    return render(request, 'post.html', context)

@login_required
def add_comment(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return redirect('latestposts')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            
            # Dodaj logikę dodawania komentarza
            comment = Comment(post=post, user=request.user, nickname=request.user.userprofile.nickname, content=content)
            comment.save()
            
            # Sprawdź, czy komentarz został pomyślnie dodany
            if comment.id:
                # Przekieruj na tę samą stronę postu
                return redirect('post', slug=post.slug)
        
        # Jeśli formularz jest nieprawidłowy, przekazujemy go do kontekstu
        # razem z postem i wyświetlimy komunikat o błędzie
        return render(request, 'body/post.html', {'post': post, 'form': form})
    
    # Jeśli żądanie nie jest POST, przekieruj na stronę postu
    form = CommentForm()
    return redirect('post', slug=post.slug)
