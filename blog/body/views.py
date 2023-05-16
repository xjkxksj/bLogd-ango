from django.shortcuts import render

def frontpage(request):
    return render(request, 'body/frontpage.html')

def authors(request):
    return render(request, 'body/authors.html')

def login(request):
    return render(request, 'body/login.html')

def register(request):
    return render(request, 'body/register.html')

def favourites(request):
    return render(request, 'body/favourites.html')
