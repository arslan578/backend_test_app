from django.contrib.auth import get_user_model
from django.db import models
# Create your models here.

User = get_user_model()


class ItemCount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    item_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class Item(models.Model):
    field_a = models.CharField(max_length=256)
    field_b = models.CharField(max_length=256)
    item_count = models.ForeignKey(ItemCount, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

