from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models.signals import post_save , pre_save
from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.shortcuts import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
import datetime

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    firstname = models.CharField(default='', max_length=100)
    lastname = models.CharField(default='', max_length=100)
    user_email = models.CharField(default='', max_length=100)

    def __str__(self):
        return self.user.username

    def save(self , *args , **kwargs):
        email_address = self.user.email
        self.user_email = email_address
        self.firstname = self.user.first_name
        self.lastname = self.user.last_name
        super().save(*args, **kwargs)


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)

    if kwargs.get('raw', False):
        post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)

