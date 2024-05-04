import os
import django
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sf_cafe.settings")
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

def create_superuser():
    super_user_email = os.getenv("SUPER_USER_EMAIL")
    super_user_password = os.getenv("SUPER_USER_PASSWORD")

    if not super_user_email or not super_user_password:
        raise ValueError("Você deve definir SUPER_USER_EMAIL e SUPER_USER_PASSWORD no arquivo .env")

    if User.objects.filter(email=super_user_email).exists():
        return
        
    User.objects.create_superuser(super_user_email, super_user_password,)


if __name__ == "__main__":
    create_superuser()
