from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if  (not email):
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.is_member = False
        user.is_approved = True
        user.save(using=self._db)
        return user

    def create_librarian(self, email, password=None):
        user = self.create_user(email, password=password)
        user.is_member = False
        user.is_lib = True
        user.is_approved = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(max_length=120, unique=True)
    is_lib = models.BooleanField(default=False)
    is_member = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class PendingMemberAccounts(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)

    def __str__(self):
        return self.name