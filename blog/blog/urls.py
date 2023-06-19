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
    latestposts_view,
    post_view,
    private_post_view,
    tag_posts_view,
    search_view,
)
from django.conf import settings
from django.conf.urls.static import static

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
    path('latestposts/', latestposts_view, name='latestposts'),
    path('post/<slug:slug>/', post_view, name='post'),
    path('post/private/<slug:slug>/', private_post_view, name='private_post'),
    path('tag/<str:tag_name>/', tag_posts_view, name='tag_posts'),
    path('search/', search_view, name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
