# coding=utf-8
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
