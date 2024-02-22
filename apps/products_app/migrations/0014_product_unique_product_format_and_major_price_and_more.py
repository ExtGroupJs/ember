# Generated by Django 4.1.7 on 2023-04-24 04:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products_app", "0013_product_in_production"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="product",
            constraint=models.UniqueConstraint(
                fields=("name", "distribution_format", "wholesale_price"),
                name="unique_product_format_and_major_price",
            ),
        ),
        migrations.AddConstraint(
            model_name="product",
            constraint=models.CheckConstraint(
                check=models.Q(("cost__gt", models.F("wholesale_price"))),
                name="The cost has to be smaller than the wholesale_price",
            ),
        ),
    ]
