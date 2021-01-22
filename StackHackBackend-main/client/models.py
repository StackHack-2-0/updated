from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, EmailValidator, MaxLengthValidator, URLValidator
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_id = models.CharField(null=True,max_length=20,blank=True)
    name = models.CharField(max_length=100,null=True)
    organization = models.CharField(max_length=100,null=True)
    employee_id = models.CharField(max_length=20, null=True)
    mobile = models.CharField(null=True,max_length=20)
    email = models.EmailField(null=True,validators=[EmailValidator(message="Enter a valid Email address",code=None,whitelist=None)])
    id_card = models.ImageField(null=True,upload_to='id/')
    verified =  models.BooleanField(default=False,null=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.user.username
    class Meta:
        managed = True
