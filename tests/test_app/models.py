# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_powerbank.db.models.fields import UniqueSlugField, MarkDownField


class NamedModel(models.Model):
    name = models.CharField(max_length=150, verbose_name=_('foo'))
    slug = UniqueSlugField(source_field='name')


class Markdown(models.Model):
    text = models.TextField()
    text_html = MarkDownField()
