# Generated by Django 4.1.7 on 2023-04-11 10:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("food_delivery_app", "0009_restaurantpersonnel"),
    ]

    operations = [
        migrations.RenameField(
            model_name="orderproducts", old_name="item_id", new_name="product_id",
        ),
    ]
