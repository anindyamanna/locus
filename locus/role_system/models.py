from django.contrib.auth.models import AbstractUser
from django.db import models


class Action(models.Model):
    action_name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return "Id -> {0} Name -> {1}".format(self.id, self.action_name)


class Resource(models.Model):
    # Just having res_name as a value
    resource_name = models.CharField(max_length=128)
    resource_desc = models.CharField(max_length=1024)

    def __str__(self):
        return "Id -> {0} Name -> {1}".format(self.id, self.resource_name)


class ActionResourcePair(models.Model):
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=256, unique=True, editable=False)

    def save(self, *args, **kwargs):
        self.slug = sorted("{0}---{1}".format(self.action.id, self.resource.id))
        return super().save(*args, kwargs)

    def __str__(self):
        return "Id -> {0} Name -> {1}|{2}".format(self.id, self.action.action_name, self.resource.resource_name)


class Role(models.Model):
    role_name = models.CharField(max_length=128, unique=True)
    action_resource_pairs = models.ManyToManyField(ActionResourcePair)

    def __str__(self):
        return self.role_name


class CustomUser(AbstractUser):
    # Extended django user just to have all the nitty gritty user details like username, password etc.
    roles = models.ManyToManyField(Role)
