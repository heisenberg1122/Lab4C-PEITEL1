from django.db import models

class UserRegistration(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField(unique=True) # unique=True helps prevent duplicate emails
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.email