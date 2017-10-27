# coding=utf-8
from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MaxValueValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext as __, ugettext_lazy as _

validate_date_range = RegexValidator(r"\d{4}-\d{2}-\d{2} - \d{4}-\d{2}-\d{2}", _("Please provide a date range in format: YYYY-MM-DD - YYYY-MM-DD"))


class MsisdnValidator(RegexValidator):
    def __init__(self, code=None, inverse_match=None, flags=None):
        message = _("Please enter phone number starting with a plus sign '+', then a country code and then all else. A 10 to 15 digits. Eg. +48 123 456 789")
        super(MsisdnValidator, self).__init__(r"\+(\d){10,15}", message, code, inverse_match, flags)

    def __call__(self, value):
        value = value.replace(" ", "")
        return super(MsisdnValidator, self).__call__(value)


@deconstructible
class MaxTodayDateValidator(object):
    message = _('Ensure this value is less than or equal to %(limit_value)s.')

    def __call__(self, value):
        limit_value = datetime.now().date()
        if value > limit_value:
            params = {'limit_value': limit_value, 'value': value}
            raise ValidationError(self.message, params=params)

    def __eq__(self, other):
        return isinstance(other, MaxTodayDateValidator)


@deconstructible
class MaxCurrentYearValidator(object):
    message = _('Ensure this value is less than or equal to %(limit_value)s.')

    def __call__(self, value):
        limit_value = datetime.now().year
        if value > limit_value:
            params = {'limit_value': limit_value, 'value': value}
            raise ValidationError(self.message, params=params)

    def __eq__(self, other):
        return isinstance(other, MaxCurrentYearValidator)


@deconstructible
class SmartUrlValidator(object):
    def __call__(self, value):
        if value.startswith("http://") or value.startswith("https://"):
            return value
        return "http://" + value

    def __eq__(self, other):
        return isinstance(other, SmartUrlValidator)
