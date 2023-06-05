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
    post_view
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
    path('post/<int:post_id>/', post_view, name='post')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
