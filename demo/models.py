from django.db import models
from rest_framework import serializers

class Demo(models.Model):
    content = models.CharField(max_length=20)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "demo"