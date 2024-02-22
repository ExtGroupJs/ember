from faker import Faker
from model_bakery.recipe import Recipe

from apps.users_app.models import SystemUser

faker = Faker(0)

system_user = Recipe(
    SystemUser,
    ci=faker.ssn,
    first_name=faker.first_name,
    last_name=faker.last_name,
    email=faker.email,
    username=faker.user_name,
    gender="M" if faker.boolean(chance_of_getting_true=50) else "F",
    phone_1=faker.phone_number,
    phone_2=faker.phone_number,
)
