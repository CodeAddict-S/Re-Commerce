from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import uuid
import re
from utils.models import BaseModel

def check_valid_email(email):
    return bool(re.fullmatch('^.+@.+[.].+$', email))

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create a regular user with email and password."""
        if len(password) <= 5 or password.isdigit():
            raise ValueError("Password is too weak")
        if not check_valid_email(email):
            raise ValueError('Email is not correct')
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create a superuser with all permissions."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model using email instead of username"""
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    activation_token = models.UUIDField(default=uuid.uuid4, editable=False, null=True, blank=True)
    profile = models.FileField(null=True, blank=True)

    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(max_length=30000, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email
    
class Merchant(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

class MerchantApplication(BaseModel):
    description = models.TextField(max_length=80000)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    