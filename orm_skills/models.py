from django.db import models
from .models_ex.annotation_aggregation_like_excel_models import Product, OrderLog

class Blog(models.Model):
    name = models.CharField(max_length=50)


class Category(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="category")
    name = models.CharField(max_length=50)


class Post(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="post"
    )
    writer = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

