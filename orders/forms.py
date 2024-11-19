from django import forms

from .models import Payment, Order, OrderedFood



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["first_name", "last_name", "email", "phone", "address", "country", "state", "city", "pin_code"]