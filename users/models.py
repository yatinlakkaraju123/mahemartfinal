from django.db import models
from django.contrib.auth.models import AbstractUser 
# Create your models here.
class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True,blank=True)
    DOB = models.DateField(null=True)

#class Profile(AbstractUser):
   # user = models.OneToOneField(User , on_delete=models.CASCADE)
