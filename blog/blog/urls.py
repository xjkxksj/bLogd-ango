from django.contrib import admin
from django.urls import path
from body.views import (
    frontpage_view,
    authors_view,
    login_view,
    register_view,
    favourites_view,
    account_view,
    logout_view,
    newpost_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', frontpage_view, name='frontpage'),
    path('authors/', authors_view, name='authors'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('favourites/', favourites_view, name='favourites'),
    path('account/', account_view, name='account'),
    path('logout/', logout_view, name='logout'),
    path('newpost/', newpost_view, name='newpost'),
]
