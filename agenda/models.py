from django.db import models
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True)
    telephone = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    show = models.BooleanField(default=True)
    media = models.ImageField(blank=True, upload_to='media/%Y%m%d')

    def __str__(self) -> str:
        return self.name