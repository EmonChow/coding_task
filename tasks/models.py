from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class todo(models.Model):
    status_choices = [("C", "Completed"), ("P", "Pending")]
    priority_choices = [
        ("1", "High"),
        ("2", "Medium"),
        ("3", "Low"),
    ]
    title = models.CharField(max_length=30)
    status = models.CharField(max_length=2, choices=status_choices)
    date = models.DateTimeField(default=timezone.now)
    priority = models.CharField(max_length=6, choices=priority_choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)


class image(models.Model):
    images = models.FileField(upload_to="images/")
    todo = models.ForeignKey(todo, on_delete=models.CASCADE)
