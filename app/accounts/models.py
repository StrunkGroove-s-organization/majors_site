from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

from django.db import models
from datetime import datetime


class MyUserManager(BaseUserManager):
    def _create_user(self, email, username, password, **extra_fields):

        if not email:
            raise ValueError("Email field must be set.")

        if not username:
            raise ValueError("username field must be set.")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password):
        return self._create_user(email, username, password)

    def create_superuser(self, email, username, password):
        return self._create_user(
            email,
            username,
            password,
            is_staff=True,
            is_superuser=True,
            has_infinity_subscription=True,
            type_subscription='infinity'
        )


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, unique=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    has_infinity_subscription = models.BooleanField(default=False)
    subscription_start = models.DateTimeField(default=datetime(2000, 1, 1))
    subscription_end = models.DateTimeField(default=datetime(2000, 1, 1))
    type_subscription = models.CharField(max_length=50, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyUserManager()

    def __str__(self):
        return self.username
