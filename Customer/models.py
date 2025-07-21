from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class CustomerDetails(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    phone = models.IntegerField(unique=True)
    photo = models.ImageField(upload_to='customers')
    address = models.TextField(max_length=300)
    def __str__(self):
        return self.first_name