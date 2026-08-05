from datetime import date

import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework import status

from apps.products_app.models import (
    Classification,
    Destination,
    Entity,
    GroupingPackaging,
    IndividualPackaging,
    MeasurementUnit,
    Plan,
    Product,
    Production,
)


@pytest.mark.django_db
class TestProductionMonthCumulativeReport:
    @staticmethod
    def _login(client):
        client.login(username="admin", password="1qazxsw2")

    @staticmethod
    def _report_url():
        return reverse("production-month-cumulative-report")

    @staticmethod
    def _build_grouping_packaging(suffix):
        measurement_unit = baker.make(
            MeasurementUnit,
            name=f"Mililitro {suffix}",
            symbol=f"ml{suffix}",
            mililiters=1,
        )
        individual_packaging = baker.make(
            IndividualPackaging,
            name=f"Botella 350 {suffix}",
            capacity=350,
            measurement_unit=measurement_unit,
            is_grouping_packaging=False,
        )
        return baker.make(
            GroupingPackaging,
            name=f"Caja 12 {suffix}",
            capacity=12,
            individual_packaging=individual_packaging,
        )

    def _build_report_dataset(self, year=2025):
        destination = baker.make(Destination, name=f"Destino {year}")
        plan_unit = baker.make(
            MeasurementUnit,
            name=f"Hectolitro {year}",
            symbol=f"hl{year}",
            mililiters=100000,
            used_for_planning=True,
        )
        distribution_format = self._build_grouping_packaging(year)

        root_classification = baker.make(Classification, name=f"Bebidas {year}")
        child_classification = baker.make(
            Classification,
            name=f"Refrescos {year}",
            parent=root_classification,
        )
        other_classification = baker.make(Classification, name=f"Conservas {year}")

        ueb_a = baker.make(
            Entity,
            name=f"UEB A {year}",
            email=f"ueb-a-{year}@test.local",
        )
        ueb_b = baker.make(
            Entity,
            name=f"UEB B {year}",
            email=f"ueb-b-{year}@test.local",
        )

        plan_a = baker.make(
            Plan,
            name=f"Plan Refrescos {year}",
            ueb=ueb_a,
            destiny=destination,
            product_kind=child_classification,
            measurement_unit=plan_unit,
            year=year,
            jan_quantity=100,
            feb_quantity=80,
            mar_quantity=25,
        )
        plan_b = baker.make(
            Plan,
            name=f"Plan Conservas {year}",
            ueb=ueb_b,
            destiny=destination,
            product_kind=other_classification,
            measurement_unit=plan_unit,
            year=year,
            jan_quantity=30,
            feb_quantity=40,
            mar_quantity=50,
        )

        product_a = baker.make(
            Product,
            name=f"Cola {year}",
            classification=child_classification,
        )
        product_b = baker.make(
            Product,
            name=f"Naranja {year}",
            classification=child_classification,
        )
        product_c = baker.make(
            Product,
            name=f"Pasta {year}",
            classification=other_classification,
        )

        baker.make(
            Production,
            name=f"Prod Cola Ene {year}",
            product=product_a,
            plan=plan_a,
            distribution_format=distribution_format,
            quantity=10,
            wholesale_price=10,
            cost=5,
            production_date=date(year, 1, 10),
        )
        baker.make(
            Production,
            name=f"Prod Cola Feb {year}",
            product=product_a,
            plan=plan_a,
            distribution_format=distribution_format,
            quantity=15,
            wholesale_price=11,
            cost=5,
            production_date=date(year, 2, 10),
        )
        baker.make(
            Production,
            name=f"Prod Naranja Feb {year}",
            product=product_b,
            plan=plan_a,
            distribution_format=distribution_format,
            quantity=5,
            wholesale_price=12,
            cost=5,
            production_date=date(year, 2, 11),
        )
        baker.make(
            Production,
            name=f"Prod Pasta Mar {year}",
            product=product_c,
            plan=plan_b,
            distribution_format=distribution_format,
            quantity=7,
            wholesale_price=13,
            cost=5,
            production_date=date(year, 3, 5),
        )

        baker.make(
            Production,
            name=f"Prod Otro Ano {year}",
            product=product_a,
            plan=plan_a,
            distribution_format=distribution_format,
            quantity=99,
            wholesale_price=14,
            cost=5,
            production_date=date(year - 1, 1, 1),
        )
        baker.make(
            Production,
            name=f"Prod Sin UEB {year}",
            product=product_a,
            plan=baker.make(
                Plan,
                name=f"Plan sin UEB {year}",
                ueb=None,
                destiny=destination,
                product_kind=child_classification,
                measurement_unit=plan_unit,
                year=year,
            ),
            distribution_format=distribution_format,
            quantity=22,
            wholesale_price=15,
            cost=5,
            production_date=date(year, 4, 1),
        )

        return {
            "year": year,
            "root_classification": root_classification,
            "child_classification": child_classification,
            "other_classification": other_classification,
            "ueb_a": ueb_a,
            "ueb_b": ueb_b,
            "plan_a": plan_a,
            "plan_b": plan_b,
            "product_a": product_a,
            "product_b": product_b,
            "product_c": product_c,
        }

    def test_requires_year_parameter(self, client):
        self._login(client)

        response = client.get(self._report_url())

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"error": "El parámetro 'year' es obligatorio"}

    def test_returns_bad_request_for_invalid_month(self, client):
        self._login(client)

        response = client.get(self._report_url(), {"year": 2025, "month": 13})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Parámetros inválidos" in response.data["error"]
        assert "Mes inválido" in response.data["error"]

    def test_returns_annual_cumulative_report_grouped_by_ueb_and_classification(
        self, client
    ):
        dataset = self._build_report_dataset()
        self._login(client)

        response = client.get(self._report_url(), {"year": dataset["year"]})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["year"] == dataset["year"]
        assert response.data["month"] is None
        assert len(response.data["report"]) == 2

        first_ueb_report = response.data["report"][0]
        assert first_ueb_report["ueb_id"] == dataset["ueb_a"].id
        assert first_ueb_report["ueb_name"] == dataset["ueb_a"].name
        assert len(first_ueb_report["classifications"]) == 1

        first_classification = first_ueb_report["classifications"][0]
        assert first_classification["classification_id"] == dataset[
            "child_classification"
        ].id
        assert first_classification["classification_name"] == dataset[
            "child_classification"
        ].name
        assert (
            first_classification["classification_hierarchy"]
            == dataset["child_classification"]._str_full_hierarchy()
        )
        assert first_classification["monthly_totals"]["enero"] == 10
        assert first_classification["monthly_totals"]["febrero"] == 20
        assert first_classification["annual_total"] == 30
        assert first_classification["plan_monthly_totals"]["enero"] == 100
        assert first_classification["plan_monthly_totals"]["febrero"] == 80
        assert first_classification["plan_monthly_totals"]["marzo"] == 25
        assert first_classification["plan_annual_total"] == 205
        assert len(first_classification["products"]) == 2

        first_product = first_classification["products"][0]
        second_product = first_classification["products"][1]
        assert first_product["product_id"] == dataset["product_a"].id
        assert first_product["monthly_production"]["enero"] == 10
        assert first_product["monthly_production"]["febrero"] == 15
        assert first_product["annual_total"] == 25
        assert second_product["product_id"] == dataset["product_b"].id
        assert second_product["monthly_production"]["febrero"] == 5
        assert second_product["annual_total"] == 5

        second_ueb_report = response.data["report"][1]
        second_classification = second_ueb_report["classifications"][0]
        assert second_ueb_report["ueb_id"] == dataset["ueb_b"].id
        assert second_classification["classification_id"] == dataset[
            "other_classification"
        ].id
        assert second_classification["monthly_totals"]["marzo"] == 7
        assert second_classification["annual_total"] == 7
        assert second_classification["plan_monthly_totals"]["enero"] == 30
        assert second_classification["plan_monthly_totals"]["febrero"] == 40
        assert second_classification["plan_monthly_totals"]["marzo"] == 50
        assert second_classification["plan_annual_total"] == 120

    def test_returns_single_month_report_when_month_filter_is_sent(self, client):
        dataset = self._build_report_dataset(year=2026)
        self._login(client)

        response = client.get(
            self._report_url(), {"year": dataset["year"], "month": 2}
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["month"] == 2
        assert len(response.data["report"]) == 1

        first_classification = response.data["report"][0]["classifications"][0]
        assert list(first_classification["monthly_totals"].keys()) == ["febrero"]
        assert first_classification["monthly_totals"]["febrero"] == 20
        assert first_classification["annual_total"] == 20
        assert first_classification["plan_monthly_totals"] == {"febrero": 80.0}
        assert first_classification["plan_annual_total"] == 80.0

        first_product = first_classification["products"][0]
        second_product = first_classification["products"][1]
        assert first_product["monthly_production"] == {"febrero": 15}
        assert first_product["annual_total"] == 15
        assert second_product["monthly_production"] == {"febrero": 5}
        assert second_product["annual_total"] == 5

    def test_applies_ueb_product_and_classification_filters(self, client):
        dataset = self._build_report_dataset(year=2027)
        self._login(client)

        response = client.get(
            self._report_url(),
            {
                "year": dataset["year"],
                "plan__ueb": dataset["ueb_a"].id,
                "product": dataset["product_b"].id,
                "product__classification": dataset["child_classification"].id,
            },
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["report"]) == 1

        ueb_report = response.data["report"][0]
        assert ueb_report["ueb_id"] == dataset["ueb_a"].id
        assert len(ueb_report["classifications"]) == 1

        classification_report = ueb_report["classifications"][0]
        assert classification_report["classification_id"] == dataset[
            "child_classification"
        ].id
        assert len(classification_report["products"]) == 1
        assert classification_report["products"][0]["product_id"] == dataset[
            "product_b"
        ].id
        assert classification_report["products"][0]["annual_total"] == 5
        assert classification_report["monthly_totals"] == {"febrero": 5.0}
        assert classification_report["annual_total"] == 5
        assert classification_report["plan_monthly_totals"]["enero"] == 100
        assert classification_report["plan_monthly_totals"]["febrero"] == 80