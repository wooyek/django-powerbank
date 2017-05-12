# coding=utf-8
# Copyright 2015 Brave Labs sp. z o.o.
import unittest
from unittest import TestCase

import sys

from datetime import date, datetime

from django.conf import settings
from django.test import Client
from . import factories


class AssertionsMx(TestCase):
    def assertNoFormErrors(self, response, form_context_key='form'):
        if not hasattr(response, 'context_data'):
            return
        forms = response.context_data.get(form_context_key)
        if forms is None:
            return
        if not isinstance(forms, list):
            forms = [forms]
        for form in forms:
            if isinstance(form.errors, dict):
                self.assertDictEqual({}, form.errors)
            else:
                self.assertListEqual([], form.errors)


class MigrationsCheck(TestCase):
    def test_missing_migrations(self):
        from django.db import connection
        from django.apps.registry import apps
        from django.db.migrations.executor import MigrationExecutor
        executor = MigrationExecutor(connection)
        from django.db.migrations.autodetector import MigrationAutodetector
        from django.db.migrations.state import ProjectState
        autodetector = MigrationAutodetector(
            executor.loader.project_state(),
            ProjectState.from_apps(apps),
        )
        changes = autodetector.changes(graph=executor.loader.graph)
        self.assertEqual({}, changes)


class AdminUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = factories.UserFactory.create(is_superuser=True, is_staff=True, username='django_administrator')
        self.client.force_login(self.user, settings.AUTHENTICATION_BACKENDS[0])


class StaffUserTestCase(AssertionsMx, TestCase):
    def setUp(self):
        self.client = Client()
        self.user = factories.UserFactory.create(is_superuser=False, is_staff=True)
        self.client.force_login(self.user, settings.AUTHENTICATION_BACKENDS[0])


class UserTestCase(TestCase, AssertionsMx):
    def setUp(self):
        self.client = Client()
        self.user = self.person.user
        self.client.force_login(self.user, settings.AUTHENTICATION_BACKENDS[0])
