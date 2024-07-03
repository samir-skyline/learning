from django.db import models


class student(models.Model):
    name = models.CharField(max_length=22)
    email = models.EmailField(blank=True, unique=True)
    password = models.CharField(max_length=20)
    isAdmin = models.BooleanField(default=True)

    def __str__(self):
        return self.name