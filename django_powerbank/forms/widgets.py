# coding=utf-8
# Copyright 2015 Brave Labs sp. z o.o.
# All rights reserved.
#
# This source code and all resulting intermediate files are CONFIDENTIAL and
# PROPRIETY TRADE SECRETS of Brave Labs sp. z o.o.
# Use is subject to license terms. See NOTICE file of this project for details.
from django.core.urlresolvers import reverse_lazy
from django.forms import widgets
from django.forms.widgets import Input


class Typeahead(Input):

    def __init__(self, attrs=None, url=None):
        super().__init__(attrs)
        self.url = url

    def build_attrs(self, extra_attrs=None, **kwargs):
        extra_attrs["class"] = extra_attrs.get("class", "") + " typeahead"
        extra_attrs.setdefault("data-url", self.url)
        attrs = super().build_attrs(extra_attrs, **kwargs)
        return attrs


class PhoneInput(widgets.TextInput):
    input_type = 'tel'
