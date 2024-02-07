from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from django.conf import settings
import requests

# Register your models here.

admin.site.register(models.Enrollment)

class PaymentAdmin(admin.ModelAdmin):
    actions = ["process_refund"]

    def process_refund(self, request, queryset):
        for payment in queryset:
            try:
                # Example API call
                headers = {"Authorization": f"Bearer {settings.PAYZE_API_KEY}"}
                response = requests.put(
                    "https://api.payze.io/payment/refund",
                    headers=headers,
                    json={"paymentId": payment.payze_paymentId}
                )
                if response.status_code == 200:
                    self.message_user(request, "Refund processed successfully for payment ID: {}".format(payment.pk))
                else:
                    self.message_user(request, "Failed to process refund for payment ID: {}. Error: {}".format(payment.pk, response.text))
            except Exception as e:
                self.message_user(request, "An error occurred while processing the refund for payment ID: {}. Error: {}".format(payment.pk, str(e)))

    process_refund.short_description = "Refund selected payments"
    
    list_display = ('id', 'amount', 'status', 'enrollment', 'created_at', 'updated_at')

    # Adding filters
    list_filter = ('status', 'created_at', 'updated_at', 'enrollment')

    # Search functionality (optional, but useful)
    search_fields = ('status', 'enrollment__user__email', 'payze_transactionId', 'payze_paymentId')

admin.site.register(models.Payment, PaymentAdmin)


class BitCampUserAdmin(UserAdmin):
    # Use the default fields from UserAdmin and add 'phone_number'
    fieldsets = UserAdmin.fieldsets + (
        (('Additional Info'), {'fields': ('phone_number',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (('Additional Info'), {'fields': ('phone_number',)}),
    )

    list_display = ('email', 'first_name', 'last_name', 'phone_number')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')

admin.site.register(models.BitCampUser, BitCampUserAdmin)