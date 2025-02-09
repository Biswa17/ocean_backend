from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Organization(models.Model):
    organization_id = models.AutoField(primary_key=True)
    organization_name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.organization_name

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, phone_number, organization, password=None):
        """
        Create and return a regular user with email, phone_number, and organization.
        """
        if not username:
            raise ValueError("The Username field must be set")
        if not email:
            raise ValueError("The Email field must be set")
        if not phone_number:
            raise ValueError("The Phone Number field must be set")
        if not organization:
            raise ValueError("The Organization field must be set")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            phone_number=phone_number,
            organization=organization
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, phone_number, organization, password=None):
        """
        Create and return a superuser with email, phone_number, and organization.
        """
        user = self.create_user(
            username=username,
            email=email,
            phone_number=phone_number,
            organization=organization,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)  # Ensure email is unique
    phone_number = models.CharField(max_length=15, unique=True)  # Ensure phone number is unique
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'  # The field used for authentication
    REQUIRED_FIELDS = ['email', 'phone_number', 'organization']  # These are required when creating a user

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
