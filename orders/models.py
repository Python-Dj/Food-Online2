import simplejson as json

from django.db import models

from accounts.models import User
from menu.models import FoodItem
from vendor.models import Vendor


request_obj = ""

class Payment(models.Model):
    PAYMENT_METHOD = (
        ("PayPal", "PayPal"),
        ("RazorPay", "RazorPay"), # Only for India.
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    transaction_id = models.CharField(max_length=100)
    payment_method = models.CharField(choices=PAYMENT_METHOD, max_length=100)
    amount = models.CharField(max_length=10)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id
    

class Order(models.Model):
    STATUS = (
        ("New", "New"),
        ("Accepted", "Accepted"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled")
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="orders")
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    vendors = models.ManyToManyField(Vendor, blank=True, related_name="orders")
    order_number = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=200)
    country = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=50)
    total = models.FloatField()
    tax_data = models.JSONField(blank=True, help_text="Data format: {tax_type: {tax_percentage: tax_amount}}", null=True)
    total_data = models.JSONField(null=True, blank=True)
    total_tax = models.FloatField(null=True)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(choices=STATUS, max_length=15, default="New")
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
    
    
    def order_place_to(self):
        return ", ".join([str(i) for i in self.vendors.all()])
    
    
    def get_total_by_vendor(self):
        vendor = Vendor.objects.get(user=request_obj.user)
        if self.total_data:
            total_data = json.loads(self.total_data)
            data = total_data.get(str(vendor.id))
            subtotal = float(data.pop("subtotal"))
            tax_data = data
            tax_amount = 0
            for key, value in data.items():
                for amt in value.values():
                    tax_amount += float(amt)
            total = subtotal + tax_amount
            return dict(total=total, tax_data=tax_data, subtotal=subtotal)
        
    
    def __str__(self):
        return self.order_number
    

class OrderedFood(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fooditem = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fooditem.food_title
