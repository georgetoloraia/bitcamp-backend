# Generated by Django 5.0.1 on 2024-01-13 00:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_enrollment_payze_payment_url_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enrollment',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='payment_date',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='receipt_file',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='user',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='verified',
        ),
        migrations.AddField(
            model_name='enrollment',
            name='user',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='cardMask',
            field=models.CharField(default='null mask', max_length=32, verbose_name='Card Mask'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='enrollment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='accounts.enrollment'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='paymentUrl',
            field=models.URLField(default='www.bitcamp.ge', verbose_name='Payment URL'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='payze_transactionId',
            field=models.CharField(default='none', max_length=128, verbose_name='Payze Transaction ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.CharField(default='Pending', max_length=128, verbose_name='Payment status'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='token',
            field=models.CharField(default='No token', max_length=128, verbose_name='Token'),
            preserve_default=False,
        ),
    ]