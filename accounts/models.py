from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    visit_count = models.IntegerField(null=True)
    time = models.DateTimeField(null=True)
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    # altitude = models.CharField(max_length=10, null=True)
    