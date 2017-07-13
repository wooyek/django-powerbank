# coding=utf-8
# Copyright 2015 Brave Labs sp. z o.o.
# All rights reserved.
#
# This source code and all resulting intermediate files are CONFIDENTIAL and
# PROPRIETY TRADE SECRETS of Brave Labs sp. z o.o.
# Use is subject to license terms. See NOTICE file of this project for details.
from django.forms import widgets
from django.forms.fields import DateField, CharField

from django_powerbank.forms.widgets import Typeahead, PhoneInput


class DateRangeField(DateField):
    widget = widgets.Input

    def __init__(self, input_formats=None, *args, **kwargs):
        super().__init__(input_formats, *args, **kwargs)

    def to_python(self, value):
        start, end = value.split(" - ")
        start, end = super().to_python(start), super().to_python(end)
        return start, end


class PhoneField(CharField):
    widget = PhoneInput


class TypeaheadField(CharField):
    widget = Typeahead
