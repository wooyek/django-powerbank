# coding=utf-8
import logging

from django import db
from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.forms import widgets
from django.utils.translation import ugettext as __, ugettext_lazy as _
from django.utils.encoding import force_text


class Typeahead(widgets.Input):
    def __init__(self, attrs=None, url=None):
        super().__init__(attrs)
        self.url = url

    def build_attrs(self, base_attrs, extra_attrs=None, **kwargs):
        extra_attrs["class"] = extra_attrs.get("class", "") + " typeahead"
        extra_attrs.setdefault("data-url", self.url)
        attrs = super().build_attrs(base_attrs, extra_attrs=extra_attrs, **kwargs)
        return attrs


class PhoneInput(widgets.TextInput):
    input_type = 'tel'


class SelectizeBase(widgets.Input):
    def __init__(self, attrs=None, url=None, allow_create=False, value_field='text', label_field='text', search_field='text', plugins=[]):
        self.url = url
        self.allow_create = allow_create
        self.value_field = value_field
        self.label_field = label_field
        self.search_field = search_field
        self.plugins = plugins
        attrs = attrs or {}
        attrs.setdefault('placeholder', _('Type a name to search and pick a value'))
        super().__init__(attrs)

    def build_attrs(self, base_attrs, extra_attrs=None, **kwargs):
        extra_attrs["class"] = extra_attrs.get("class", "") + " "
        extra_attrs.setdefault("data-url", self.url)
        attrs = super().build_attrs(base_attrs, extra_attrs=extra_attrs, **kwargs)
        return attrs

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        selectize = context.setdefault('selectize', {})
        selectize['url'] = self.url
        selectize['allow_create'] = self.allow_create
        selectize['value_field'] = self.value_field
        selectize['label_field'] = self.label_field
        selectize['search_field'] = self.search_field
        selectize['plugins'] = self.plugins
        return context


class SelectizeSelect(SelectizeBase, widgets.Select):
    """
    A selectize.js field

    It requires selectize.js and headjs to be avaialable in the browser. See a template below to se why.
    You can provide your own template to use selectize.js in a different way.
    """
    template_name = 'django_powerbank/forms/widgets/selectize/select.html'

    def optgroups(self, name, value, attrs=None):
        """Return a list of optgroups for this widget."""
        default = (None, [], 0)
        groups = [default]
        # We must add at least one 'selected' option or widget will show nothing.
        for v in value:
            if not v:
                continue
            if hasattr(self.choices, 'queryset'):
                item = self.choices.queryset.filter(id=v).first()
                if item:
                    label = item.name
                else:
                    label = force_text(v)
            else:
                label = force_text(v)
            subgroup = default[1]
            subgroup.append(self.create_option(
                name, v, label, True, 0,
                subindex=None, attrs=attrs,
            ))
        return groups


class SelectizeTags(SelectizeBase):
    template_name = 'django_powerbank/forms/widgets/selectize/tags.html'
