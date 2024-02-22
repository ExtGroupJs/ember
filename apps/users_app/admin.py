import csv
from django.contrib import admin

from apps.users_app.models import (
    EmployeeArea,
    EmployeeResponsability,
    SystemEmail,
    SystemUser,
)


@admin.register(SystemUser)
class SystemUserAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "photo",
        "ci",
        "gender",
        "area",
        "responsability",
        "phone_1",
    ]
    fields = [
        "username",
        "email",
        "first_name",
        "last_name",
        "photo",
        "ci",
        "gender",
        "area",
        "responsability",
        "phone_1",
    ]

    def load_csv_file(self, request):
        # Load the CSV file
        with open("my_csv_file.csv") as f:
            reader = csv.reader(f)
            for row in reader:
                print(row)

    def get_actions(self, request):
        # Add a new action to the admin interface
        actions = super().get_actions(request)
        actions["load_csv_file"] = (self.load_csv_file, "Load CSV file", "Description")
        return actions


@admin.register(EmployeeArea)
class EmployeeAreaAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ("name", "description")
    fields = ("name", "description")


@admin.register(EmployeeResponsability)
class EmployeeResponsabilityAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ("name", "description")
    fields = ("name", "description")


@admin.register(SystemEmail)
class SystemEmailAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ("user", "topic", "text", "sent_date", "attachment")
    fields = ("user", "topic", "text", "attachment")
