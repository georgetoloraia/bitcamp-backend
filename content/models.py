from django.db import models

# Create your models here.
    
class Mentor(models.Model):
    fullname = models.CharField(
        max_length=32,
        blank=False,
        null=False
    )
    
    biography = models.CharField(
        verbose_name="Information about the mentor",
        max_length=256,
        blank=True,
        null=True
    )

class Service(models.Model):
    title = models.CharField(
        verbose_name="Service title",
        max_length=32,
        blank=False,
        null=False
    )
    
    price = models.DecimalField(
        verbose_name="Price of service",
        max_digits=6,
        decimal_places=2,
        blank=False,
        null=False
    )
    
    mentors = models.ManyToManyField(
        to=Mentor,
        blank=True
    )

class Program(models.Model):
    title = models.CharField(
        verbose_name="Program title",
        max_length=32,
        blank=False,
        null=False
    )
    
    services = models.ManyToManyField(
        verbose_name="Program services",
        to=Service,
        blank=False
    )