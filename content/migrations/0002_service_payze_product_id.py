# Generated by Django 5.0.1 on 2024-01-11 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='payze_product_id',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='Payze Product ID'),
        ),
    ]