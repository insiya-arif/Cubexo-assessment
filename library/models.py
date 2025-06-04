from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timedelta
from django.utils import timezone


# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email

class Book(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='books/')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ReadingList(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.email} - {self.book.title}"

def ten_minutes_from_now():
    return timezone.now() + timedelta(minutes=10)

class OTP(models.Model):
    user_email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=ten_minutes_from_now)

    def __str__(self):
        return f"{self.user_email} - {self.code}"


