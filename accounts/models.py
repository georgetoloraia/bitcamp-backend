from django.contrib.auth.models import AbstractUser
from django.db import models
from content import models as content


class BitCampUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        default=None
    )
        
    first_name = models.CharField(
        max_length=150,
        blank=False,
        null=False
    )
    
    last_name = models.CharField(
        max_length=150,
        blank=False,
        null=False
    )
    
    phone_number = models.CharField(
        max_length=16
    )
    
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False
    )
    
    def __str__(self):
        return self.email

class DiscordUser(models.Model):
    first_name = models.CharField(
        max_length=150,
        blank=False,
        null=False
    )
    
    last_name = models.CharField(
        max_length=150,
        blank=False,
        null=False
    )
    
    personal_id = models.CharField(
        max_length=32,
        blank=False,
        null=False
    )
    
    phone_number = models.CharField(
        max_length=32,
        blank=False,
        null=False
    )
    
    discord_id = models.CharField(
        verbose_name="Unique identifier for Discord user",
        max_length=18,
        unique=True,
        primary_key=True,
        null=False,
        blank=False
    )
    
    onboarding_channel_id = models.CharField(
        verbose_name="ID of the private Discord channel for onboarding",
        max_length=18,
        unique=True
    )
    
    is_registered = models.BooleanField(
        verbose_name="Status of user's registration",
        default=False
    )

    def __str__(self):
        return self.discord_id

class Enrollment(models.Model):
    name = models.CharField(
        max_length=128
    )

    enrollment_date = models.DateField(
        auto_now=True
    )

    enrollment_cancel_date = models.DateField(
        null=True,
        default=None
    )

    user_id = models.OneToOneField(
        to=BitCampUser,
        on_delete=models.CASCADE,
        null=True
    )

    service_id = models.OneToOneField(
        to=content.Service,
        on_delete=models.SET_NULL,
        null=True
    )

    program_id = models.OneToOneField(
        to=content.Program,
        on_delete=models.SET_NULL,
        null=True
    )

    mentor_id = models.OneToOneField(
        to=content.Mentor,
        on_delete=models.SET_NULL,
        null=True
    )

    status = models.CharField(
        max_length=16
    )

    payze_subscription_id = models.CharField(
        max_length=255, null=True, blank=True
    )

    payze_payment_url = models.URLField(
        max_length=255, null=True, blank=True
    )
    
# Stores information about payment receipts
class Payment(models.Model):
    user = models.OneToOneField(
        to=DiscordUser,
        on_delete=models.SET_NULL,
        blank=False,
        null=True
    )
    
    receipt_file = models.FileField(
        verbose_name="Store the uploaded receipt",
        blank=False
    )
    
    amount = models.DecimalField(
        verbose_name="Amount paid",
        max_digits=16,
        decimal_places=2,
        blank=False
    )
    
    payment_date = models.DateField(
        auto_now_add=True
    )
    
    verified = models.BooleanField(
        verbose_name="Status of payment verification",
        default=False
    )