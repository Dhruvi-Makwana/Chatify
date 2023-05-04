from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    profile_photo = models.ImageField(upload_to="profile_photo/")
    mobile_number = PhoneNumberField(unique=True)
    is_online = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.username


class Group(models.Model):
    name = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now=True)
    user = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name


class Chat(models.Model):
    message = models.CharField(max_length=5000)
    created = models.DateTimeField(auto_now=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_messages"
    )
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username} to {self.receiver.username}"
