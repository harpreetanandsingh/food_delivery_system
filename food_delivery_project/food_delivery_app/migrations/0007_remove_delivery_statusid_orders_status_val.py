# Generated by Django 4.1.7 on 2023-04-08 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("food_delivery_app", "0006_alter_status_status_val"),
    ]

    operations = [
        migrations.RemoveField(model_name="delivery", name="statusId",),
        migrations.AddField(
            model_name="orders",
            name="status_val",
            field=models.CharField(
                choices=[
                    ("Processing", "Processing"),
                    ("Out For Delivery", "Out For Delivery"),
                    ("Delivered", "Delivered"),
                ],
                default="Processing",
                max_length=255,
            ),
        ),
    ]