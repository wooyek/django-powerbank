# coding=utf-8
import factory
from django.contrib.auth import get_user_model
from faker import Faker

from django_powerbank import models

fake = Faker()


class UserFactory(factory.DjangoModelFactory):
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    username = factory.Sequence(lambda n: fake.user_name() + str(n))
    is_staff = False
    is_active = True

    class Meta:
        model = get_user_model()


class SomeModelFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.SomeModel


class AndAnotherFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.AndAnother
