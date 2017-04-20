# coding=utf-8
# Copyright 2015 Brave Labs sp. z o.o.
# All rights reserved.
#
# This source code and all resulting intermediate files are CONFIDENTIAL and
# PROPRIETY TRADE SECRETS of Brave Labs sp. z o.o.
# Use is subject to license terms. See NOTICE file of this project for details.
import logging
from django.core.urlresolvers import reverse_lazy
from django.forms import widgets


class Typeahead(widgets.Input):

    def __init__(self, attrs=None, url=None):
        super().__init__(attrs)
        self.url = url

    def build_attrs(self, base_attrs, extra_attrs=None, **kwargs):
        extra_attrs["class"] = extra_attrs.get("class", "") + " typeahead"
        extra_attrs.setdefault("data-url", self.url)
        attrs = super().build_attrs(base_attrs, extra_attrs=extra_attrs, **kwargs)
        return attrs


class Selectize(widgets.Select):
    """
    A selectize.js field
    
    It requires selectize.js and headjs to be avaialable in the browser. See a template below to se why. 
    You can provide your own template to use selectize.js in a different way. 
    """
    template_name = 'django_powerbank/forms/widgets/selectize.html'

    def __init__(self, attrs=None, url=None):
        super().__init__(attrs)
        self.url = url

    def build_attrs(self, base_attrs, extra_attrs=None, **kwargs):
        extra_attrs["class"] = extra_attrs.get("class", "") + " "
        attrs = super().build_attrs(base_attrs, extra_attrs=extra_attrs, **kwargs)
        return attrs

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['url'] = self.url
        return context

    def options(self, name, value, attrs=None):
        raise Exception()
        logging.debug("self.choices: %s", self.choices)
        print(self.choices)
        label = self.choices.filter(id=value).get().name
        print(label)
        logging.debug("label: %s", label)
        yield self.create_option(
            name, value, label, True, 0,
            subindex=0, attrs=attrs,
        )

    def optgroups(self, name, value, attrs=None):
        """Return a list of optgroups for this widget."""
        default = (None, [], 0)
        groups = [default]
        for v in value:
            if not v:
                continue
            label = self.choices.queryset.filter(id=v).get().name
            subgroup = default[1]
            subgroup.append(self.create_option(
                name, v, label, True, 0,
                subindex=None, attrs=attrs,
            ))
        return groups


class PhoneInput(widgets.TextInput):
    input_type = 'tel'
