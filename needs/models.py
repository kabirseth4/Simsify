from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from datetime import datetime, timezone
from django.utils.translation import gettext_lazy as _

import math


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email


class Need(models.Model):
    name = models.CharField(max_length=30)
    max_level = models.PositiveIntegerField()
    current_level = models.PositiveIntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    negative_need = models.BooleanField(default=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='needs')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.current_level > self.max_level:
            self.current_level = self.max_level
        super(Need, self).save(*args, **kwargs)

    def get_level(self):
        now = datetime.now(timezone.utc)
        change = math.floor(
            (now - self.last_updated).total_seconds() / 60)

        if self.negative_need:
            updated_level = min(self.current_level + change, self.max_level)
        else:
            updated_level = max(self.current_level - change, 0)

        return (updated_level / self.max_level) * 100


class Action(models.Model):
    name = models.CharField(max_length=100)
    value = models.SmallIntegerField()
    related_need = models.ForeignKey(
        Need, on_delete=models.CASCADE, related_name='actions')

    def __str__(self):
        return self.name
