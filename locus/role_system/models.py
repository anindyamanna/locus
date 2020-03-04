from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    role_name = models.CharField(max_length=128, unique=True)
    read_allowed = models.BooleanField(default=False)
    write_allowed = models.BooleanField(default=False)
    delete_allowed = models.BooleanField(default=False)

    def __str__(self):
        return self.role_name


class CustomUser(AbstractUser):
    # Extended django user just to have all the nitty gritty user details like username, password etc.
    roles = models.ManyToManyField(Role)


class Resource(models.Model):
    # Just having res_name as a value
    res_name = models.CharField(max_length=1024)

    def __str__(self):
        return self.res_name
