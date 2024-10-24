from django.db import models
from vendor.models import Vendor


class Category(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="categories")
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"

    def clean(self):
        self.category_name = self.category_name.capitalize()

    def __str__(self):
        return self.category_name
    

class FoodItem(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    food_title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to="foodimages")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.food_title
    
