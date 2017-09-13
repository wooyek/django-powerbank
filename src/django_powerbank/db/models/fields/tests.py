# coding=utf-8
import unittest

from django.test import SimpleTestCase

from . import UniqueSlugField


class UniqueSlugFieldTests(SimpleTestCase):
    @unittest.skip("needs a mockup application model to test")
    def test_counts_up(self):
        a = models.Organization.objects.create(name="name")
        b = models.Organization.objects.create(name="name")
        c = models.Organization.objects.create(name="name")
        self.assertEqual("name", a.slug)
        self.assertEqual("name-1", b.slug)
        self.assertEqual("name-2", c.slug)
