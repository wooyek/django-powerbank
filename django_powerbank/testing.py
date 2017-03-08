# coding=utf-8
# Copyright 2015 Brave Labs sp. z o.o.
import unittest
from unittest import TestCase

import sys


class AssertionsMx(TestCase):

    def assertNoFormErrors(self, response, form_context_key='form'):
        if not hasattr(response, 'context_data'):
            return
        form = response.context_data.get(form_context_key)
        if form is None:
            return
        if isinstance(form.errors, dict):
            self.assertDictEqual({}, form.errors)
        else:
            self.assertListEqual([], form.errors)


class MigrationsCheck(TestCase):
    @unittest.skipUnless(sys.platform == 'win32', "Only test locally for now")
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
