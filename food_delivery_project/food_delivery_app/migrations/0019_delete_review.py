# Generated by Django 4.1.7 on 2023-04-11 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("food_delivery_app", "0018_delete_status"),
    ]

    operations = [
        migrations.DeleteModel(name="Review",),
    ]
