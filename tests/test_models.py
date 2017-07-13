#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-powerbank
------------

Tests for `django-powerbank` models module.
"""

from django.test import TestCase

from django_powerbank import models
from tests import factories


class TestDjango_powerbank(TestCase):

    def test_something(self):
        assert models
        factories.UserFactory
