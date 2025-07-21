from django.db import models
from Customer.models import CustomerDetails
# Create your models here.


class Categories(models.Model):
    category = models.CharField(max_length=30, unique=True)
    link = models.SlugField(unique=True)
    def __str__(self):
        return self.category


class GreeneryProducts(models.Model):
    product = models.CharField(max_length=50, unique=True)
    content = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, blank=True)
    category = models.ForeignKey(Categories, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    image = models.ImageField(upload_to='Greenery_Products')
    stock = models.IntegerField()
    def __str__(self):
        return self.product




class Feedback(models.Model):
    user = models.ForeignKey(CustomerDetails, on_delete=models.CASCADE)
    feedback = models.TextField()
    product = models.ForeignKey(GreeneryProducts, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"