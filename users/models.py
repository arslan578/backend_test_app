from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.


class User(AbstractUser):
    entered = models.BooleanField(default=False)

    def __str__(self):
        return self.username
