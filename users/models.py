from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
from django.contrib.auth.models import User

User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False


class Profile(models.Model):
    owner = models.OneToOneField(
        User, on_delete=models.CASCADE)
    dob = models.DateField(auto_now_add=True)
    phone_number = models.CharField(max_length=200)
    subscription = models.BooleanField(default=False)


class Security(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)


class Verification(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=User)
def create_security(sender, instance, created, **kwargs):
    if created:
        Security.objects.create(owner=instance)


@receiver(post_save, sender=User)
def save_security(sender, instance, **kwargs):
    instance.security.save()
