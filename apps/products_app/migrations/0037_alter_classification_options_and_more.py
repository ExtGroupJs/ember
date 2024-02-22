# Generated by Django 4.2.1 on 2023-09-16 19:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products_app", "0036_alter_groupingpackaging_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="classification",
            options={
                "verbose_name": "clasificación",
                "verbose_name_plural": "clasificaciones",
            },
        ),
        migrations.AlterModelOptions(
            name="destination",
            options={"verbose_name": "destino", "verbose_name_plural": "destinos"},
        ),
        migrations.AlterModelOptions(
            name="format",
            options={"verbose_name": "formato", "verbose_name_plural": "formatos"},
        ),
        migrations.AlterModelOptions(
            name="measurementunit",
            options={
                "verbose_name": "unidad de medida",
                "verbose_name_plural": "unidades de medida",
            },
        ),
        migrations.AlterModelOptions(
            name="product",
            options={"verbose_name": "producto", "verbose_name_plural": "productos"},
        ),
        migrations.AlterModelOptions(
            name="production",
            options={
                "verbose_name": "producción",
                "verbose_name_plural": "producciones",
            },
        ),
        migrations.AlterField(
            model_name="individualpackaging",
            name="material",
            field=models.CharField(
                choices=[("P", "plástico"), ("V", "vidrio")],
                default="V",
                max_length=1,
                verbose_name="Material",
            ),
        ),
    ]
