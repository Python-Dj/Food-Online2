from django import forms
from .models import Category, FoodItem
from vendor.validators import allow_image_only_validator


class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields = ["category_name", "description"]


class FoodForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={"class": "btn btn-info w-100"}), validators=[allow_image_only_validator])

    class Meta:
        model = FoodItem
        fields = ["category", "food_title", "description", "price", "image", "is_available"]

    