from django.db import models

# Create your models here.

# This model doesnt inherit from django.contrib.auth.models.AbstractUser
# because this is not a traditional account with usernames and passwords
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
