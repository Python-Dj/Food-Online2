from django import forms
from accounts.models import User


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["firstName", "lastName", "phone_number"]