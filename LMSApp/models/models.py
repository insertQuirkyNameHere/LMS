from tkinter import CASCADE
from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()

# Create your models here.
class Librarian(models.Model):
    name = models.CharField(max_length=50)
    userObj = models.OneToOneField(UserModel, unique=True, on_delete=models.CASCADE)

class Member(models.Model):
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=10)
    userObj = models.OneToOneField(UserModel, unique=True, on_delete=models.CASCADE)