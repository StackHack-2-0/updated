from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import os
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.core.validators import MinLengthValidator, EmailValidator, MaxLengthValidator, URLValidator

class Food(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    food_code = models.CharField(null=True,max_length=20)
    name = models.CharField(max_length=100,null=True)
    description = models.CharField(max_length=300,null=True)
    price = models.IntegerField(null=True)
    image = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.food_code) + " " + self.name

    class Meta:
        managed = True
