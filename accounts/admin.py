from django.contrib import admin
from . import models

# Register your models here.
    
admin.site.register(models.DiscordUser)
admin.site.register(models.BitCampUser)
admin.site.register(models.Enrollment)