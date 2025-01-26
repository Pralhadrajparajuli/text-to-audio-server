from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import tensorflow as tf


# Custom User Manager
class CustomUserManager(models.Manager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hashing the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    def get_by_natural_key(self, email):
        """Override to return user by email (natural key)."""
        return self.get(email=email)
    

    
class CustomUser(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Use email as the unique identifier
    REQUIRED_FIELDS = []  # No required fields apart from email

    def __str__(self):
        return self.email

    def set_password(self, raw_password):
        """Hash the password before saving it."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Check if the given password matches the hashed password."""
        return check_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        # Ensure that the user has a valid email and password
        if not self.email:
            raise ValidationError(_("Email cannot be blank"))
        if not self.password:
            raise ValidationError(_("Password cannot be blank"))
        super().save(*args, **kwargs)

    def get_full_name(self):
        """Returns the full name of the user"""
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        """Returns the short name of the user"""
        return self.first_name

    @property
    def is_authenticated(self):
        """Returns whether the user is authenticated"""
        return self.is_active

    @property
    def is_anonymous(self):
        """Returns whether the user is anonymous"""
        return not self.is_active
    

