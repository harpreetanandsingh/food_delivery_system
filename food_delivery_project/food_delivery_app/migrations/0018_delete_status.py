# Generated by Django 4.1.7 on 2023-04-11 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("food_delivery_app", "0017_alter_deliverypersonnel_availability"),
    ]

    operations = [
        migrations.DeleteModel(name="Status",),
    ]