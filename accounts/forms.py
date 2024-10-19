from typing import Any
from django import forms
from .models import User, UserProfile

from vendor.validators import allow_image_only_validator




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


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={"class": "btn btn-info"}), validators=[allow_image_only_validator])
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={"class": "btn btn-info"}), validators=[allow_image_only_validator])
    class Meta:
        model = UserProfile
        exclude = ["user", "created_at", "modified_at"]
        
    # def __init__(self, *args, **kwargs):
    #     super(UserProfileForm, self).__init__(*args, **kwargs)
    #     self.fields["latitude"].widget.attrs['readonly'] = True
    #     self.fields["longitude"].widget.attrs['readonly'] = True


    #* we can use different approach if there are so many readonly fields.
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field in ["latitude", "longitude"]:
                self.fields[field].widget.attrs["readonly"] = True