from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser




class UserManager(BaseUserManager):
    def create_user(self, firstName, lastName, username, email, password=None):
        if not email:
            raise ValueError("User must have an email address.")
        if not username:
            raise ValueError("User must have username.")
        
        user = self.model(
            firstName = firstName,
            lastName = lastName,
            username = username,
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, firstName, lastName, username, email, password=None):
        user = self.create_user(
            firstName = firstName,
            lastName = lastName,
            username = username,
            email = self.normalize_email(email),
            password = password
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    class RoleChoice(models.IntegerChoices):
        RESTAURANT = 1, 'Restaurant'
        CUSTOMER = 2, 'Customer'

    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=12, blank=True)
    role = models.CharField(choices=RoleChoice.choices, blank=True, null=True)

    # reqquired fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "firstName", "lastName"]

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_profile")
    profile_picture = models.ImageField(upload_to="users/profile_pictures",blank=True, null=True)
    cover_photo = models.ImageField(upload_to="users/cover_photos", blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    # def full_address(self):
    #     return f"{self.address_line_1}, {self.address_line_2}"

    def __str__(self) -> str:
        return (self.user.email or self.user.username)

