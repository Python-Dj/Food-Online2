from django.db import models
from accounts.models import User, UserProfile

from .utils import send_notification 



class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="vendor")
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="vendorprofile")
    vendor_name = models.CharField(max_length=50)
    vendor_slug = models.SlugField(max_length=50, unique=True)
    vendor_license = models.ImageField(upload_to="vendor/license")
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name

    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_subject = "Congratulation! Your Rasturant has been approved."
                context = {
                    "user": self.user,
                    "is_approved": self.is_approved
                }
                if self.is_approved == True:
                    send_notification(mail_subject, context)
                else:
                    mail_subject = "We're sorry! You are not eligible for publishing your food menu on our marketplace."

                    send_notification(mail_subject, context)
        return super(Vendor, self).save(*args, **kwargs)
