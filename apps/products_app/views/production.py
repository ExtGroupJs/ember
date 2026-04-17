from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from collections import defaultdict
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema

from apps.common.views import ActionsForNonDeletableItemsViewMixin, CommonViewMixin
from apps.products_app.models import Production, Plan
from apps.products_app.serializers import (
    ProductionReadSerializer,
    ProductionSerializer,
)
from apps.products_app.filters import ProductionFilter


class ProductionViewSet(
    viewsets.ModelViewSet, CommonViewMixin, ActionsForNonDeletableItemsViewMixin
):
    queryset = Production.objects.all()
    serializer_class = ProductionSerializer
    filterset_class = ProductionFilter
    ordering_fields = [field.name for field in queryset.model._meta.fields] + [
        "entity__name"
    ]

    search_fields = [
        "name",
        "product__name",
        "product__classification__name",
        "distribution_format__name",
        "entity__name",
    ]

    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ["GET"]:
            return ProductionReadSerializer
        return ProductionSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="year",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Año del reporte (obligatorio)",
                required=True,
            ),
            OpenApiParameter(
                name="month",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Mes específico (opcional, 1-12)",
                required=False,
            ),
            OpenApiParameter(
                name="plan__ueb",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Filtrar por UEB específica",
                required=False,
            ),
            OpenApiParameter(
                name="product",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Filtrar por producto específico",
                required=False,
            ),
            OpenApiParameter(
                name="product__classification",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Filtrar por clasificación",
                required=False,
            ),
        ]
    )
    @action(
        detail=False,
        methods=["GET"],
        url_name="month-cumulative-report",
        url_path="month-cumulative-report",
    )
    def month_cumulative_report(self, request, pk=None):
        """
        Genera un reporte mensual acumulado de producción por producto,
        respetando la jerarquía de clasificaciones y separado por UEB.

        Parámetros de query:
        - year: Año del reporte (obligatorio)
        - month: Mes específico (opcional, si no se indica muestra todo el año)
        - plan__ueb: Filtrar por UEB específica
        - product: Filtrar por producto específico
        - product__classification: Filtrar por clasificación
        """
        # Obtener parámetros de filtrado
        year = request.query_params.get("year")
        month = request.query_params.get("month")

        if not year:
            return Response(
                {"error": "El parámetro 'year' es obligatorio"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            year = int(year)
            if month:
                month = int(month)
                if month < 1 or month > 12:
                    raise ValueError("Mes inválido")
        except ValueError as e:
            return Response(
                {"error": f"Parámetros inválidos: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Filtrar producciones por año y aplicar filtros del queryset
        queryset = self.filter_queryset(self.get_queryset())
        productions = (
            queryset.filter(production_date__year=year)
            .select_related("product", "product__classification", "plan", "plan__ueb")
            .order_by(
                "plan__ueb__name",
                "product__classification__name",
                "product__name",
                "production_date",
            )
        )

        if month:
            productions = productions.filter(production_date__month=month)

        # Estructura para organizar los datos
        # {ueb_id: {classification_id: {product_id: {month: quantity}}}}
        report_data = defaultdict(
            lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
        )
        ueb_info = {}
        classification_info = {}
        product_info = {}

        # Procesar las producciones
        for production in productions:
            ueb = (
                production.plan.ueb if production.plan and production.plan.ueb else None
            )
            if not ueb:
                continue

            ueb_id = ueb.id
            ueb_info[ueb_id] = ueb.name

            classification = production.product.classification
            classification_id = classification.id
            classification_info[classification_id] = {
                "name": classification.name,
                "hierarchy": classification._str_full_hierarchy(),
                "parent_id": classification.parent_id
                if classification.parent
                else None,
            }

            product_id = production.product.id
            product_info[product_id] = production.product.name

            prod_month = production.production_date.month

            # Acumular cantidad
            report_data[ueb_id][classification_id][product_id][prod_month] += (
                production.quantity
            )

        # Obtener los planes correspondientes para comparar
        plans = Plan.objects.filter(year=year).select_related("product_kind", "ueb")

        if month:
            # Para un mes específico, solo consideramos ese mes del plan
            month_field = self._get_month_field_name(month)

        plan_data = defaultdict(
            lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
        )

        for plan in plans:
            if not plan.ueb:
                continue
            ueb_id = plan.ueb.id
            classification_id = plan.product_kind.id

            # Agregar los planes mensuales
            months_to_process = [month] if month else range(1, 13)
            for m in months_to_process:
                month_field = self._get_month_field_name(m)
                plan_quantity = getattr(plan, month_field, 0)
                plan_data[ueb_id][classification_id][m] += plan_quantity

        # Estructurar respuesta
        result = []

        for ueb_id in sorted(report_data.keys(), key=lambda x: ueb_info.get(x, "")):
            ueb_data = {
                "ueb_id": ueb_id,
                "ueb_name": ueb_info[ueb_id],
                "classifications": [],
            }

            for classification_id in sorted(report_data[ueb_id].keys()):
                classification_data = {
                    "classification_id": classification_id,
                    "classification_name": classification_info[classification_id][
                        "name"
                    ],
                    "classification_hierarchy": classification_info[classification_id][
                        "hierarchy"
                    ],
                    "products": [],
                    "monthly_totals": defaultdict(float),
                    "annual_total": 0,
                    "plan_monthly_totals": defaultdict(float),
                    "plan_annual_total": 0,
                }

                for product_id in sorted(report_data[ueb_id][classification_id].keys()):
                    monthly_data = report_data[ueb_id][classification_id][product_id]
                    annual_total = sum(monthly_data.values())

                    product_data = {
                        "product_id": product_id,
                        "product_name": product_info[product_id],
                        "monthly_production": {
                            self._get_month_name(m): monthly_data.get(m, 0)
                            for m in (range(1, 13) if not month else [month])
                        },
                        "annual_total": annual_total,
                    }

                    classification_data["products"].append(product_data)

                    # Acumular en totales de clasificación
                    for m, qty in monthly_data.items():
                        classification_data["monthly_totals"][
                            self._get_month_name(m)
                        ] += qty
                    classification_data["annual_total"] += annual_total

                # Agregar datos del plan
                plan_monthly = plan_data.get(ueb_id, {}).get(classification_id, {})
                for m in range(1, 13) if not month else [month]:
                    plan_qty = plan_monthly.get(m, 0)
                    month_name = self._get_month_name(m)
                    classification_data["plan_monthly_totals"][month_name] = plan_qty
                    classification_data["plan_annual_total"] += plan_qty

                ueb_data["classifications"].append(classification_data)

            result.append(ueb_data)

        return Response(
            {"year": year, "month": month, "report": result}, status=status.HTTP_200_OK
        )

    def _get_month_field_name(self, month_number):
        """Convierte número de mes a nombre de campo en el modelo Plan"""
        month_fields = {
            1: "jan_quantity",
            2: "feb_quantity",
            3: "mar_quantity",
            4: "apr_quantity",
            5: "may_quantity",
            6: "jun_quantity",
            7: "jul_quantity",
            8: "aug_quantity",
            9: "sep_quantity",
            10: "oct_quantity",
            11: "nov_quantity",
            12: "dec_quantity",
        }
        return month_fields.get(month_number, "jan_quantity")

    def _get_month_name(self, month_number):
        """Convierte número de mes a nombre en español"""
        month_names = {
            1: "enero",
            2: "febrero",
            3: "marzo",
            4: "abril",
            5: "mayo",
            6: "junio",
            7: "julio",
            8: "agosto",
            9: "septiembre",
            10: "octubre",
            11: "noviembre",
            12: "diciembre",
        }
        return month_names.get(month_number, "enero")
