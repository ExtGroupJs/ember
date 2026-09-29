import random
from datetime import date

from django.core.management.base import BaseCommand

from apps.products_app.models import (
    Classification,
    Destination,
    Entity,
    Format,
    GroupingPackaging,
    IndividualPackaging,
    MeasurementUnit,
    Plan,
    Product,
    Production,
)

SEEDED_YEARS = [2025, 2026]

CLASSIFICATION_TREE = {
    "Bebidas y refrescos": {
        "Refrescos": [
            "Refresco cola",
            "Refresco naranja",
            "Refresco limón",
            "Refresco uva",
        ],
        "Aguas": [
            "Agua mineral",
            "Agua con gas",
        ],
        "Aguas saborizadas": [
            "Agua saborizada limón",
        ],
        "Zumos y néctares": [
            "Néctar guayaba",
            "Zumo de naranja",
        ],
        "Bebidas energéticas": [
            "Energética clásica",
            "Energética zero",
        ],
        "Bebidas isotónicas": [
            "Isotónica limón",
        ],
        "Bebidas alcohólicas": [
            "Cerveza ligera",
            "Ron",
        ],
    },
}

UEBS = [
    ("UEB Planta Norte", "planta.norte@ember.local", "53211234", "53211235"),
    ("UEB Planta Sur", "planta.sur@ember.local", "53221234", "53221235"),
    ("UEB Embotelladora Central", "central@ember.local", "53231234", "53231235"),
]

DESTINATIONS = [
    "Mercado Nacional",
    "Zona Turística",
    "Exportación",
]

FORMATS = [
    "Caja",
    "A granel",
    "Paquete retractilado",
    "Botella suelta",
]

INDIVIDUAL_PACKAGING = [
    {"name": "Botella PET 355", "capacity": 355, "unit": "ml", "material": "P"},
    {"name": "Botella retornable 1000", "capacity": 1000, "unit": "ml", "material": "V"},
    {"name": "Lata 355", "capacity": 355, "unit": "ml", "material": "P"},
    {"name": "Garrafón 5000", "capacity": 5000, "unit": "ml", "material": "P"},
]

GROUPING_PACKAGING = [
    ("Caja 24 x 355", "Botella PET 355", 24),
    ("Caja 12 x 1000", "Botella retornable 1000", 12),
    ("Sixpack 6 x 355", "Botella PET 355", 6),
    ("Lata pack 24", "Lata 355", 24),
    ("Garrafón 5L suelto", "Garrafón 5000", 1),
    ("Caja retornable 6", "Botella retornable 1000", 6),
]

# productos de la fábrica: nombre -> clasificación final
PRODUCTS = {
    "Kola Cristal": "Refresco cola",
    "Naranja Burbujas": "Refresco naranja",
    "Limón Helado": "Refresco limón",
    "Uva Negra": "Refresco uva",
    "Agua Pura": "Agua mineral",
    "Soda Club": "Agua con gas",
    "Saborízate Limón": "Agua saborizada limón",
    "Guayabita Néctar": "Néctar guayaba",
    "Naranja Natural": "Zumo de naranja",
    "Energiza Original": "Energética clásica",
    "Energiza Zero": "Energética zero",
    "Suerox Limón": "Isotónica limón",
    "Cerveza Rubia Especial": "Cerveza ligera",
    "Ron Caney": "Ron",
}

# volumen base mensual del plan (hectolitros) por clasificación final
PLAN_SCALE = {
    "Refresco cola": 180,
    "Refresco naranja": 120,
    "Refresco limón": 80,
    "Refresco uva": 60,
    "Agua mineral": 150,
    "Agua con gas": 70,
    "Agua saborizada limón": 45,
    "Néctar guayaba": 90,
    "Zumo de naranja": 75,
    "Energética clásica": 65,
    "Energética zero": 40,
    "Isotónica limón": 55,
    "Cerveza ligera": 200,
    "Ron": 30,
}

# estacionalidad mensual (verano pico)
MONTH_FACTOR = [
    0.85, 0.90, 0.95, 1.00, 1.10, 1.20,
    1.30, 1.25, 1.00, 0.95, 0.90, 1.05,
]

# precios base por producto: (costo, precio mayorista)
PRICES = {
    "Kola Cristal": (8.50, 18.00),
    "Naranja Burbujas": (7.90, 16.50),
    "Limón Helado": (7.50, 15.50),
    "Uva Negra": (7.50, 15.50),
    "Agua Pura": (3.20, 8.00),
    "Soda Club": (4.10, 9.50),
    "Saborízate Limón": (5.20, 12.00),
    "Guayabita Néctar": (9.80, 21.00),
    "Naranja Natural": (9.20, 20.00),
    "Energiza Original": (12.00, 28.00),
    "Energiza Zero": (12.50, 29.00),
    "Suerox Limón": (10.50, 24.00),
    "Cerveza Rubia Especial": (14.00, 32.00),
    "Ron Caney": (35.00, 75.00),
}


class Command(BaseCommand):
    help = (
        "Crea datos de demostración de una fábrica de bebidas y refrescos "
        "(UEBs, clasificaciones, envases, productos, planes y producciones). "
        "Usar --reset para regenerar los datos de los años sembrados."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Elimina y vuelve a crear los planes y producciones sembrados.",
        )

    def handle(self, *args, **options):
        self._seed_measurement_units()
        self._seed_classifications()
        self._seed_destinations()
        self._seed_formats()
        self._seed_entities()
        self._seed_packaging()
        self._seed_products()
        self._seed_plans_and_productions(reset=options["reset"])
        self.stdout.write(
            self.style.SUCCESS(
                "Datos de la fábrica de bebidas sembrados correctamente."
            )
        )

    def _get_or_create(self, model, defaults=None, **kwargs):
        obj, created = model.objects.get_or_create(
            defaults=defaults or {}, **kwargs
        )
        return obj, created

    def _seed_measurement_units(self):
        hl, _ = self._get_or_create(
            MeasurementUnit,
            name="Hectolitro",
            symbol="hl",
        )
        hl.used_for_planning = True
        hl.save()

    def _seed_classifications(self):
        self.classifications = {}
        for root_name, children in CLASSIFICATION_TREE.items():
            root, _ = self._get_or_create(Classification, name=root_name)
            self.classifications[root_name] = root
            for parent_name, leaf_names in children.items():
                parent, _ = self._get_or_create(
                    Classification, defaults={"parent": root}, name=parent_name
                )
                if parent.parent is None:
                    parent.parent = root
                    parent.save()
                self.classifications[parent_name] = parent
                for leaf_name in leaf_names:
                    leaf, _ = self._get_or_create(
                        Classification,
                        defaults={"parent": parent},
                        name=leaf_name,
                    )
                    if leaf.parent is None:
                        leaf.parent = parent
                        leaf.save()
                    self.classifications[leaf_name] = leaf

    def _seed_destinations(self):
        self.destinations = {}
        for name in DESTINATIONS:
            self.destinations[name], _ = self._get_or_create(Destination, name=name)

    def _seed_formats(self):
        self.formats = {}
        for name in FORMATS:
            self.formats[name], _ = self._get_or_create(Format, name=name)

    def _seed_entities(self):
        self.entities = {}
        for name, email, phone_1, phone_2 in UEBS:
            self.entities[name], _ = self._get_or_create(
                Entity,
                name=name,
                email=email,
                phone_1=phone_1,
                phone_2=phone_2,
            )

    def _seed_packaging(self):
        self.individual_packaging = {}
        units = {u.symbol: u for u in MeasurementUnit.objects.all()}
        for item in INDIVIDUAL_PACKAGING:
            obj, _ = self._get_or_create(
                IndividualPackaging,
                name=item["name"],
                defaults={
                    "capacity": item["capacity"],
                    "measurement_unit": units[item["unit"]],
                    "material": item["material"],
                },
            )
            self.individual_packaging[item["name"]] = obj

        self.grouping_packaging = {}
        for name, indiv_name, capacity in GROUPING_PACKAGING:
            obj, _ = self._get_or_create(
                GroupingPackaging,
                name=name,
                defaults={
                    "capacity": capacity,
                    "individual_packaging": self.individual_packaging[indiv_name],
                },
            )
            self.grouping_packaging[name] = obj

    def _seed_products(self):
        self.products = {}
        for product_name, classification_name in PRODUCTS.items():
            obj, _ = self._get_or_create(
                Product,
                name=product_name,
                classification=self.classifications[classification_name],
                defaults={"format": self.formats["Caja"]},
            )
            self.products[product_name] = obj

    def _seed_plans_and_productions(self, reset=False):
        if reset:
            deleted_plans = Plan.objects.filter(
                name__startswith="PLAN ",
                year__in=SEEDED_YEARS,
            )
            deleted_plans.delete()

        distribution_options = list(self.grouping_packaging.values())
        used_keys = set(
            Production.objects.all().values_list(
                "product_id", "distribution_format_id", "wholesale_price"
            )
        )

        for year in SEEDED_YEARS:
            if Plan.objects.filter(
                year=year,
                ueb__in=self.entities.values(),
                product_kind__in=self.classifications.values(),
            ).exists():
                self.stdout.write(
                    f"  Año {year}: ya sembrado, se omite (use --reset)."
                )
                continue

            plans = []
            for ueb in self.entities.values():
                for classification_name, scale in PLAN_SCALE.items():
                    classification = self.classifications[classification_name]
                    plan, _ = self._get_or_create(
                        Plan,
                        name=f"PLAN {ueb.name} - {classification_name} - {year}",
                        defaults={
                            "ueb": ueb,
                            "destiny": self.destinations["Mercado Nacional"],
                            "product_kind": classification,
                            "year": year,
                            "measurement_unit": MeasurementUnit.objects.get(
                                symbol="hl"
                            ),
                        },
                    )
                    year_factor = 0.9 if year == 2025 else 1.0
                    quantities = [
                        max(
                            1,
                            round(
                                scale * MONTH_FACTOR[m - 1] * year_factor
                            ),
                        )
                        for m in range(1, 13)
                    ]
                    setattr(plan, "jan_quantity", quantities[0])
                    setattr(plan, "feb_quantity", quantities[1])
                    setattr(plan, "mar_quantity", quantities[2])
                    setattr(plan, "apr_quantity", quantities[3])
                    setattr(plan, "may_quantity", quantities[4])
                    setattr(plan, "jun_quantity", quantities[5])
                    setattr(plan, "jul_quantity", quantities[6])
                    setattr(plan, "aug_quantity", quantities[7])
                    setattr(plan, "sep_quantity", quantities[8])
                    setattr(plan, "oct_quantity", quantities[9])
                    setattr(plan, "nov_quantity", quantities[10])
                    setattr(plan, "dec_quantity", quantities[11])
                    plan.save()
                    plans.append(plan)

            productions = []
            for plan in plans:
                product = self.products[
                    next(
                        name
                        for name, classification_name in PRODUCTS.items()
                        if classification_name == plan.product_kind.name
                    )
                ]
                cost, price = PRICES[product.name]
                for month, plan_qty in enumerate(
                    [
                        plan.jan_quantity,
                        plan.feb_quantity,
                        plan.mar_quantity,
                        plan.apr_quantity,
                        plan.may_quantity,
                        plan.jun_quantity,
                        plan.jul_quantity,
                        plan.aug_quantity,
                        plan.sep_quantity,
                        plan.oct_quantity,
                        plan.nov_quantity,
                        plan.dec_quantity,
                    ],
                    start=1,
                ):
                    seed = hash((plan.id, month)) % 1000
                    rng = random.Random(seed)
                    compliance = round(0.70 + (seed % 100) / 100 * 0.60, 2)
                    total_quantity = max(0, round(plan_qty * compliance))
                    records = rng.randint(1, 3)
                    pieces = []
                    for _ in range(records):
                        pieces.append(rng.randint(1, 6))
                    pieces_total = sum(pieces)
                    produced_so_far = 0
                    for i, piece in enumerate(pieces):
                        if i == records - 1:
                            quantity = total_quantity - produced_so_far
                        else:
                            quantity = round(total_quantity * piece / pieces_total)
                        produced_so_far += quantity
                        if quantity <= 0:
                            continue
                        distribution_format = distribution_options[
                            (month + plan.id) % len(distribution_options)
                        ]
                        wholesale_price = price + (month % 3)
                        key = (product.id, distribution_format.id, wholesale_price)
                        while key in used_keys:
                            wholesale_price = round(wholesale_price + 0.50, 2)
                            key = (product.id, distribution_format.id, wholesale_price)
                        used_keys.add(key)
                        productions.append(
                            Production(
                                name=f"{product.name[:18]} {month}/{plan.year}",
                                product=product,
                                plan=plan,
                                distribution_format=distribution_format,
                                quantity=quantity,
                                cost=cost,
                                wholesale_price=wholesale_price,
                                extra_info=(
                                    f"Producción {month}/{plan.year} para "
                                    f"{plan.destiny.name}"
                                ),
                                active=True,
                                production_date=date(year, month, rng.randint(1, 28)),
                            )
                        )
            Production.objects.bulk_create(productions)
            self.stdout.write(
                self.style.SUCCESS(
                    f"  Año {year}: {len(plans)} planes y "
                    f"{len(productions)} producciones creadas."
                )
            )
