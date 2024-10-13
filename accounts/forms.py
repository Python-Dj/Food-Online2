from typing import Any
from django import forms
from .models import User




class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), max_length=50)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), max_length=50)

    class Meta:
        model = User
        fields = ["firstName", "lastName", "username", "email", "password", "confirm_password"]

    
    def clean(self):
        data = super().clean()
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password does not match"
            )
