# Generated by Django 4.1.7 on 2023-04-07 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("food_delivery_app", "0004_deliverypersonnel_addr_id"),
    ]

    operations = [
        migrations.DeleteModel(name="personnelAddr",),
    ]
