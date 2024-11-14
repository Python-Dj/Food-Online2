from django.db import models
from accounts.models import User, UserProfile
from datetime import time, datetime

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
    

    def is_open(self):
        today_day = datetime.today().isoweekday()
        current_op_hrs = OpeningHour.objects.filter(vendor=self, day=today_day)

        current_time = datetime.now().strftime("%H:%M:%S")
        
        for hour in current_op_hrs:
            if hour.is_closed:
                return False
            start = str(datetime.strptime(hour.from_hour, "%I:%M %p").time())
            end = str(datetime.strptime(hour.to_hour, "%I:%M %p").time())
            if current_time > start and current_time < end:
                return True
            else:
                return False


    def __str__(self):
        return self.vendor_name


class OpeningHour(models.Model):
    class DayChoices(models.IntegerChoices):
        MONDAY =    1
        TUESDAY =   2
        WEDNESDAY = 3
        THURSDAY =  4
        FRIDAY =    5
        SATAURDAY = 6
        SUNDAY =    7
    
    HOURS_OF_DAYS_24 = [
        (time(h, m).strftime("%I:%M %p"), time(h, m).strftime("%I:%M %p"))
        for h in range(0, 24)
        for m in (0, 30)
    ]
    
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DayChoices)
    from_hour = models.CharField(choices=HOURS_OF_DAYS_24, max_length=10, blank=True)
    to_hour = models.CharField(choices=HOURS_OF_DAYS_24, max_length=10, blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ("day", "-from_hour")
        unique_together = ("vendor", "day", "from_hour", "to_hour")

    def __str__(self):
        return self.get_day_display()