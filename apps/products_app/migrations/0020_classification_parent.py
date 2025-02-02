# Generated by Django 4.1.7 on 2023-05-05 21:39

import django.db.models.deletion
from django.db import migrations, models, transaction


@transaction.atomic
def create_clasifications(apps, schema_editor):
    Classification = apps.get_model("products_app", "Classification")
    Classification.objects.all().delete()
    alcoholics, _ = Classification.objects.get_or_create(name="Bebidas alcohólicas")

    Classification.objects.bulk_create(
        [
            Classification(name="Rones", parent=alcoholics),
            Classification(name="Aguardiente", parent=alcoholics),
            Classification(name="Otras", parent=alcoholics),
        ]
    )
    wine, _ = Classification.objects.get_or_create(name="Vinos")

    Classification.objects.bulk_create(
        [
            Classification(name="Vino Dulce", parent=wine),
            Classification(name="Vino Seco", parent=wine),
            Classification(name="Vino Semidulce", parent=wine),
        ]
    )
    soft_drink, _ = Classification.objects.get_or_create(name="Refrescos")

    Classification.objects.bulk_create(
        [
            Classification(name="Refresco a granel", parent=soft_drink),
            Classification(name="Refresco en bolsa", parent=soft_drink),
            Classification(name="Refresco Concentrado convertido", parent=soft_drink),
        ]
    )
    soft_drink_cc, _ = Classification.objects.get_or_create(
        name="Refresco Concentrado convertido"
    )

    Classification.objects.bulk_create(
        [
            Classification(
                name="Refresco Concentrado convertido a granel", parent=soft_drink_cc
            ),
            Classification(
                name="Refresco Concentrado convertido envasado", parent=soft_drink_cc
            ),
        ]
    )
    soft_drink_cc_env, _ = Classification.objects.get_or_create(
        name="Refresco Concentrado convertido envasado"
    )

    Classification.objects.bulk_create(
        [
            Classification(
                name="Refresco Concentrado convertido envasado en pomo",
                parent=soft_drink_cc_env,
            ),
            Classification(
                name="Refresco Concentrado convertido envasado en vidrio",
                parent=soft_drink_cc_env,
            ),
            Classification(
                name="Refresco Concentrado convertido envasado en dispensa",
                parent=soft_drink_cc_env,
            ),
        ]
    )
    vinager, _ = Classification.objects.get_or_create(name="Vinagre")

    Classification.objects.bulk_create(
        [
            Classification(name="Vinagre a granel", parent=vinager),
            Classification(name="Vinagre embotellado", parent=vinager),
        ]
    )

    beer, _ = Classification.objects.get_or_create(name="Cerveza")

    Classification.objects.bulk_create(
        [
            Classification(name="Cerveza a granel", parent=beer),
            Classification(name="Cerveza embotellada", parent=beer),
        ]
    )
    alternative_productions, _ = Classification.objects.get_or_create(
        name="Producciones alternativas"
    )


def remove_clasifications(apps, schema_editor):
    Classification = apps.get_model("products_app", "Classification")
    Classification.objects.filter(parent__isnull=False).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("products_app", "0019_entity_phone_1_entity_phone_2"),
    ]

    operations = [
        migrations.AddField(
            model_name="classification",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="products_app.classification",
            ),
        ),
        migrations.RunPython(create_clasifications, remove_clasifications),
    ]
