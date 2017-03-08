# coding=utf-8
import logging
from django.db import connections
from django.db.models import QuerySet


class ApproxQuerySet(QuerySet):
    def _approx_count(self, default):
        raise NotImplementedError('Do not use this class itself.')

    def count(self):
        if self._result_cache is not None:
            if hasattr(self, '_iter') and not self._iter:
                return len(self._result_cache)

        query = self.query
        default_count = self.query.get_count

        if (query.high_mark is None and
                    query.low_mark == 0 and
                not query.where and
                not query.select and
                not query.group_by and
                not query.having and
                not query.distinct):
            return self._approx_count(default_count)

        return default_count(using=self.db)

    @classmethod
    def wrap_query(cls, qry):
        return qry._clone(klass=cls)


class TableStatusQuerySet(ApproxQuerySet):
    def _approx_count(self, default_count):
        # For MySQL, by Nova
        # http://stackoverflow.com/a/10446271/366908
        if 'mysql' in connections[self.db].client.executable_name.lower():
            cursor = connections[self.db].cursor()
            cursor.execute('SHOW TABLE STATUS LIKE %s', (self.model._meta.db_table,))
            return cursor.fetchall()[0][4]

        # For Postgres, by Woody Anderson
        # http://stackoverflow.com/a/23118765/366908
        elif hasattr(connections[self.db].client.connection, 'pg_version'):
            parts = [p.strip('"') for p in self.model._meta.db_table.split('.')]
            cursor = connections[self.db].cursor()
            if len(parts) == 1:
                cursor.execute('SELECT reltuples::bigint FROM pg_class WHERE relname = %s', parts)
            else:
                cursor.execute('SELECT reltuples::bigint FROM pg_class c JOIN pg_namespace n ON (c.relnamespace = n.oid) WHERE n.nspname = %s AND c.relname = %s', parts)

        return default_count(using=self.db)
