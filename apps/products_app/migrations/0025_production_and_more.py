# Generated by Django 4.1.7 on 2023-05-28 19:08

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("common", "0002_historicalvault_author"),
        ("products_app", "0024_alter_groupingpackaging_historical_vault_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Production",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_timestamp",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Created timestamp"
                    ),
                ),
                (
                    "updated_timestamp",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Updated timestamp"
                    ),
                ),
                ("name", models.CharField(max_length=30, verbose_name="name")),
                ("quantity", models.PositiveIntegerField(verbose_name="amount")),
                (
                    "cost",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=6,
                        null=True,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                        verbose_name="cost",
                    ),
                ),
                (
                    "wholesale_price",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=6,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                        verbose_name="wholesale price",
                    ),
                ),
                ("active", models.BooleanField(default=True, verbose_name="active")),
            ],
            options={
                "verbose_name": "production",
                "verbose_name_plural": "productions",
            },
        ),
        migrations.RemoveConstraint(
            model_name="product",
            name="unique_product_format_and_major_price",
        ),
        migrations.RemoveField(
            model_name="product",
            name="active",
        ),
        migrations.RemoveField(
            model_name="product",
            name="cost",
        ),
        migrations.RemoveField(
            model_name="product",
            name="distribution_format",
        ),
        migrations.RemoveField(
            model_name="product",
            name="quantity",
        ),
        migrations.RemoveField(
            model_name="product",
            name="wholesale_price",
        ),
        migrations.AddField(
            model_name="production",
            name="distribution_format",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="products_app.groupingpackaging",
                verbose_name="distribution format",
            ),
        ),
        migrations.AddField(
            model_name="production",
            name="historical_vault",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="common.historicalvault",
                verbose_name="NOT USED",
            ),
        ),
        migrations.AddField(
            model_name="production",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="products_app.product",
                verbose_name="product",
            ),
        ),
        migrations.AddConstraint(
            model_name="production",
            constraint=models.UniqueConstraint(
                fields=("product", "distribution_format", "wholesale_price"),
                name="unique_product_format_and_major_price",
            ),
        ),
    ]
