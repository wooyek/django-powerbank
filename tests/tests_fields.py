# coding=utf-8

from django.test import TestCase

from tests.test_app import models


class UniqueSlugFieldTests(TestCase):
    def test_counts_up(self):
        a = models.NamedModel.objects.create(name="name")
        b = models.NamedModel.objects.create(name="name")
        c = models.NamedModel.objects.create(name="name")
        self.assertEqual("name", a.slug)
        self.assertEqual("name-1", b.slug)
        self.assertEqual("name-2", c.slug)
