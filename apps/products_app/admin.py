from django.contrib import admin

from apps.products_app.models import (
    Classification,
    Destination,
    Entity,
    Format,
    GroupingPackaging,
    IndividualPackaging,
    MeasurementUnit,
    Product,
    Production,
    Plan,
)


@admin.action(description="Archive selected objects")
def archive(modeladmin, request, queryset):
    for obj in queryset:
        obj.archive()


@admin.action(description="Des-archive selected objects")
def des_archive(modeladmin, request, queryset):
    for obj in queryset:
        obj.des_archive()


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ("id", "name", "format", "classification", "is_active")
    fields = (
        "name",
        "format",
        "classification",
    )
    actions = [archive, des_archive]


@admin.register(Production)
class ProductionAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = (
        "id",
        "name",
        "distribution_format",
        "plan",
        "wholesale_price",
        "quantity",
        "cost",
        "active",
        "is_active",
    )
    fields = (
        "name",
        "distribution_format",
        "plan",
        "wholesale_price",
        "quantity",
        "cost",
        "active",
    )
    actions = [archive, des_archive]


@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ("id", "name", "email", "enabled", "phone_1", "phone_2")
    fields = ("name", "email", "enabled", "phone_1", "phone_2")


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ("id", "name", "enabled")
    fields = ("name", "enabled")


@admin.register(Classification)
class ClassificationAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ("id", "name", "description", "parent")
    fields = ("name", "description", "parent")


@admin.register(Format)
class FormatAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ("id", "name", "description")
    fields = ("name", "description")


@admin.register(GroupingPackaging)
class GroupingPackagingAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = (
        "name",
        "description",
        "capacity",
        "individual_packaging",
        "is_active",
    )
    fields = ("name", "description", "capacity", "individual_packaging")
    actions = [archive, des_archive]


@admin.register(IndividualPackaging)
class IndividualPackagingAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = (
        "pk",
        "name",
        "description",
        "capacity",
        "measurement_unit",
        "is_grouping_packaging",
        "is_active",
    )
    fields = (
        "name",
        "description",
        "capacity",
        "measurement_unit",
        "is_grouping_packaging",
    )
    actions = [archive, des_archive]


@admin.register(MeasurementUnit)
class MeasurementUnitAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = (
        "name",
        "symbol",
        "description",
        "mililiters",
        "used_for_planning",
    )
    fields = (
        "name",
        "symbol",
        "description",
        "mililiters",
        "used_for_planning",
    )


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = (
        "pk",
        "name",
        "ueb",
        "destiny",
        "product_kind",
        "year",
        "month",
        "quantity",
        "measurement_unit",
    )
    fields = (
        "name",
        "ueb",
        "destiny",
        "product_kind",
        "year",
        "month",
        "quantity",
        "measurement_unit",
    )
