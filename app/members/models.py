from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    img_profile = models.ImageField(upload_to='user', blank=True)
    phone = models.CharField(max_length=13, blank=True)
    is_host = models.BooleanField(default=False)
    nickname = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.username
