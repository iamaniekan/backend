from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, firstName, lastName, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            firstName=firstName,
            lastName=lastName,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, firstName, lastName, password=None):
        user = self.create_user(
            email=email,
            firstName=firstName,
            lastName=lastName,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    userId = models.CharField(max_length=255, unique=True)
    firstName = models.CharField(max_length=255, null=False)
    lastName = models.CharField(max_length=255, null=False)
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=255, null=False)
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName']

    def __str__(self):
        return self.email


class Organization(models.Model):
    orgId = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(blank=True, null=True)
    users = models.ManyToManyField(User, related_name='organizations')

    def __str__(self):
        return self.name
