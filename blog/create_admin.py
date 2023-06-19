import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
django.setup()

from django.contrib.auth.models import User
from body.models import UserProfile

def create_admin():
    admin_username = 'admin'
    admin_password = 'admin123'

    admin_user, created = User.objects.get_or_create(username=admin_username)
    admin_user.set_password(admin_password)
    admin_user.is_superuser = True
    admin_user.is_staff = True
    admin_user.save()

    admin_profile, created = UserProfile.objects.get_or_create(user=admin_user, nickname='ADMIN')

    if created:
        print(f"Konto administratora zostało utworzone: {admin_username}")
    else:
        print(f"Konto administratora już istnieje: {admin_username}")

if __name__ == "__main__":
    create_admin()
