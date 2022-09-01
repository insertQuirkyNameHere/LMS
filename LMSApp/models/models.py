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

class Author(models.Model):
    name = models.CharField(max_length=256, unique=True)

class Genre(models.Model):
    genre = models.CharField(max_length=120, unique=True)

class Book(models.Model):
    title = models.CharField(max_length=520)
    authors = models.ManyToManyField(Author)
    genre = models.ManyToManyField(Genre)

