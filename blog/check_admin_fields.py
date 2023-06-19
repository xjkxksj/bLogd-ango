import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
django.setup()

from django.contrib.auth.models import User
from body.models import UserProfile

admin_username = 'admin'

try:
    admin_user = User.objects.get(username=admin_username)
    admin_profile = UserProfile.objects.get(user=admin_user)

    username = admin_user.username
    password = admin_user.password
    nickname = admin_profile.nickname

    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Nickname: {nickname}")

except User.DoesNotExist:
    print(f"Administrator o nazwie użytkownika '{admin_username}' nie istnieje.")
