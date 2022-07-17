from django.db import models


class User(models.Model):
    name = models.CharField(max_length=30)
    telegram_id = models.CharField(max_length=200)

