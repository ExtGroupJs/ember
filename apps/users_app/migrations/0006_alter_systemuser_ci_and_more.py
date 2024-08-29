# Generated by Django 4.1.7 on 2023-04-07 04:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("common", "0001_initial"),
        ("users_app", "0005_creating_superuser"),
    ]

    operations = [
        migrations.AlterField(
            model_name="systemuser",
            name="ci",
            field=models.CharField(
                default=0,
                max_length=11,
                unique=True,
                verbose_name="identification number",
            ),
            preserve_default=False,
        ),
    ]
