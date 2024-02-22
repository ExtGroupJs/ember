import random
import re

import pytest
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import CommandError
from django.urls import reverse
from model_bakery.exceptions import InvalidQuantityException
from rest_framework import status


@pytest.mark.django_db
@pytest.mark.parametrize(
    "quantity, response",
    [
        ("", CommandError),
        ("dsfgsfgs", CommandError),
        (-2, InvalidQuantityException),
    ],
)
def test_errors_in_create_test_users_command(quantity, response):
    with pytest.raises(response):
        call_command("create_test_users", quantity)


@pytest.mark.django_db
def test_create_test_users_command():
    quantity = random.randint(1, 100)
    call_command("create_test_users", str(quantity))

    user_quantity = User.objects.exclude(username="admin").count()
    assert user_quantity == quantity


@pytest.mark.django_db
def test_default_user_created():
    user = User.objects.filter(username="admin").exists()
    assert user is True


@pytest.mark.django_db
def test_users_list_available(client):
    client.login(username="admin", password="1qazxsw2")
    url = reverse("users-list")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    "username, password, status_code",
    [
        ("", "", status.HTTP_400_BAD_REQUEST),
        ("", "strong_pass", status.HTTP_400_BAD_REQUEST),
        ("user@example.com", "", status.HTTP_400_BAD_REQUEST),
        ("user@example.com", "invalid_pass", status.HTTP_400_BAD_REQUEST),
        ("admin", "1qazxsw2", status.HTTP_202_ACCEPTED),
    ],
)
def test_login_data_validation(username, password, status_code, client):
    url = reverse("users-login")
    data = {"username": username, "password": password}
    response = client.post(url, data=data)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "number, match",
    [
        ("+5333211430", True),
        ("5333211430", True),
        ("33211430", True),
        ("332114dfd30", False),
        ("+3321140000000030", True),
    ],
)
def test_phone_number_regex(number, match):
    pattern = r"^\+?\d+$"
    assert match == bool(re.match(pattern, number))
