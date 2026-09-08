from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model so roles can be extended later without a painful
    migration. Django's built-in is_staff/is_superuser already drive Django
    Admin access; `role` adds a lighter-weight tag usable from the API/JWT
    claims for the future custom admin dashboard."""

    class Role(models.TextChoices):
        SUPER_ADMIN = "super_admin", "Super Admin"
        CONTENT_EDITOR = "content_editor", "Content Editor"
        AD_MANAGER = "ad_manager", "Ad Manager"
        VIEWER = "viewer", "Viewer"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CONTENT_EDITOR)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.username
