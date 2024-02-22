# Generated by Django 4.1.7 on 2023-05-05 21:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products_app", "0020_classification_parent"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="product",
            name="cost_smaller_than_wholesale_price",
        ),
        migrations.RemoveField(
            model_name="product",
            name="in_production",
        ),
        migrations.AddField(
            model_name="product",
            name="active",
            field=models.BooleanField(default=True, verbose_name="active"),
        ),
        migrations.AlterField(
            model_name="product",
            name="cost",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=6,
                null=True,
                validators=[django.core.validators.MinValueValidator(0.0)],
                verbose_name="cost",
            ),
        ),
    ]
