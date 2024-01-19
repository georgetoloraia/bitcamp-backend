from django.contrib import admin
from . import models

# Register your models here.
    
admin.site.register(models.DiscordUser)
admin.site.register(models.BitCampUser)
admin.site.register(models.Enrollment)

class PaymentAdmin(admin.ModelAdmin):
    # List of fields to display in the admin list view
    list_display = ('id', 'amount', 'status', 'enrollment', 'created_at', 'updated_at')

    # Adding filters
    list_filter = ('status', 'created_at', 'updated_at', 'enrollment')

    # Search functionality (optional, but useful)
    search_fields = ('status', 'enrollment__user__email', 'payze_transactionId', 'payze_paymentId')

admin.site.register(models.Payment, PaymentAdmin)