from django.shortcuts import render


def frontpage(request):
    return render(request, 'body/frontpage.html')

def authors(request):
    return render(request, 'body/authors.html')
