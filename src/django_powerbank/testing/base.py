# coding=utf-8
# Copyright 2015 Brave Labs sp. z o.o.
from unittest import TestCase

from django.conf import settings
from django.test import Client

from . import factories


class AssertionsMx(object):
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
                # noinspection PyUnresolvedReferences
                self.assertDictEqual({}, form.errors)
            else:
                # noinspection PyUnresolvedReferences
                self.assertListEqual([], form.errors)


class MigrationsCheckMx(object):
    # noinspection PyPep8Naming
    def setUp(self):
        from django.utils import translation
        # noinspection PyAttributeOutsideInit
        self.saved_locale = translation.get_language()
        translation.deactivate_all()

    # noinspection PyPep8Naming
    def tearDown(self):
        if self.saved_locale is not None:
            from django.utils import translation
            translation.activate(self.saved_locale)

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
        # noinspection PyUnresolvedReferences
        self.assertEqual({}, changes)


class MigrationsCheck(MigrationsCheckMx, TestCase):
    pass


class AdminUserTestCase(AssertionsMx):
    # noinspection PyPep8Naming,PyAttributeOutsideInit
    def setUp(self):
        self.client = Client()
        self.user = factories.UserFactory.create(is_superuser=True, is_staff=True, username='django_administrator')
        self.client.force_login(self.user, settings.AUTHENTICATION_BACKENDS[0])


class StaffUserTestCase(AssertionsMx):
    # noinspection PyPep8Naming,PyAttributeOutsideInit
    def setUp(self):
        self.client = Client()
        self.user = factories.UserFactory.create(is_superuser=False, is_staff=True)
        self.client.force_login(self.user, settings.AUTHENTICATION_BACKENDS[0])


class UserTestCase(AssertionsMx):
    # noinspection PyPep8Naming,PyAttributeOutsideInit
    def setUp(self):
        self.client = Client()
        self.user = factories.UserFactory.create(is_superuser=False, is_staff=False)
        self.client.force_login(self.user, settings.AUTHENTICATION_BACKENDS[0])
