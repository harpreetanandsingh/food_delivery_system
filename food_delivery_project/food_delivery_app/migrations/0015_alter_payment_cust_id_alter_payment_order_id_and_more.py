# Generated by Django 4.1.7 on 2023-04-11 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("food_delivery_app", "0014_remove_payment_infoid_payment_cust_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="cust_id",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                to="food_delivery_app.customer",
            ),
        ),
        migrations.AlterField(
            model_name="payment",
            name="order_id",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                to="food_delivery_app.orders",
            ),
        ),
        migrations.DeleteModel(name="availability",),
    ]
