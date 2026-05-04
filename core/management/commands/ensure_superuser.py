import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "Create a superuser from DJANGO_SUPERUSER_* env vars if missing. "
        "Safe to run on every deploy (no-op when vars unset or user exists)."
    )

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")

        if not username or not password:
            self.stdout.write(
                "ensure_superuser: DJANGO_SUPERUSER_USERNAME / "
                "DJANGO_SUPERUSER_PASSWORD not set; skipping."
            )
            return

        User = get_user_model()
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.NOTICE(
                    f"ensure_superuser: user {username!r} already exists; skipping."
                )
            )
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        self.stdout.write(
            self.style.SUCCESS(f"ensure_superuser: created superuser {username!r}.")
        )
