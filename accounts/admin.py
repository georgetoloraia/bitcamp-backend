from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# Register your models here.

admin.site.register(models.Enrollment)

class PaymentAdmin(admin.ModelAdmin):
    # List of fields to display in the admin list view
    list_display = ('id', 'amount', 'status', 'enrollment', 'created_at', 'updated_at' )

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