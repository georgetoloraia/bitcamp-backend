# Generated by Django 5.0.1 on 2024-01-13 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_enrollment_user_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payze_paymentId',
            field=models.CharField(default=1234, max_length=128, verbose_name='Payze Payment ID'),
            preserve_default=False,
        ),
    ]
