# Generated by Django 4.1.7 on 2023-04-08 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("food_delivery_app", "0007_remove_delivery_statusid_orders_status_val"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payinfo",
            name="payMode",
            field=models.CharField(
                choices=[("Cash", "Cash"), ("Card", "Card")], max_length=100
            ),
        ),
    ]
