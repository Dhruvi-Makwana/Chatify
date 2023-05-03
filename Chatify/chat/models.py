from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    profile_photo = models.ImageField(upload_to="profile_photo/")
    mobile_number = PhoneNumberField(unique=True)
    online = models.BooleanField(default=False, blank=True, null=True)
