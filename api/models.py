from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    
    name = models.CharField(max_length = 50)
    

    def __str__(self):
        return super().__str__()

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)