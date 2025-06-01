from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class User1(models.Model):
  userID = models.AutoField(primary_key=True)
  email = models.CharField(max_length=255, default='abc@xyz.com')
  password = models.CharField (max_length=255, default='Abc@123')

  def __str__(self):
    return self.userID

class Book(models.Model):
  bookID = models.IntegerField()
  bookname = models.CharField(max_length=255)
  userID = models.ForeignKey(User1, on_delete=models.CASCADE)

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user
class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None): return True
    def has_module_perms(self, app_label): return True
    @property
    def is_staff(self): return self.is_admin