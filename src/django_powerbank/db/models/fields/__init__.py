# coding=utf-8
import json
import logging
from enum import IntEnum

import six
from django.core import checks
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import NOT_PROVIDED
from django.utils.crypto import salted_hmac, get_random_string
from django.utils.functional import lazy
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils.translation import ugettext as __, ugettext_lazy as _
from markdown import markdown

from django_powerbank.core.validators import MsisdnValidator
from django_powerbank.forms import fields


class PhoneField(models.CharField):
    default_validators = [MsisdnValidator()]

    def to_python(self, value):
        if value in self.empty_values:
            return None
        return super(PhoneField, self).to_python(value)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': fields.PhoneField,
        }
        defaults.update(kwargs)
        return super(PhoneField, self).formfield(**defaults)


class SourceFieldMixin(object):
    def __init__(self, source_field=None, *args, **kwargs):
        self.source_field = source_field
        super(SourceFieldMixin, self).__init__(*args, **kwargs)

    def check(self, **kwargs):
        errors = super(SourceFieldMixin, self).check(**kwargs)
        errors.extend(self._check_source_property_attribute(**kwargs))
        return errors

    def _check_source_property_attribute(self, **kwargs):
        if self.source_field is None:
            return [
                checks.Error(
                    "{} must define a 'source_property' attribute.".format(self.__class__.__name__),
                    hint=None,
                    obj=self,
                    id='misc.E001',
                )
            ]
        return []


class SecretField(SourceFieldMixin, models.CharField):
    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) or not getattr(model_instance, self.source_field):
            return super(SecretField, self).pre_save(model_instance, add)

        value = getattr(model_instance, self.source_field)
        value = salted_hmac(get_random_string(), value).hexdigest()[::2]
        setattr(model_instance, self.attname, value)
        return value


class AutoSlugField(SourceFieldMixin, models.SlugField):
    def __init__(self, source_field=None, keep_existing=False, source_fallback=False, *args, **kwargs):
        super(AutoSlugField, self).__init__(source_field, *args, **kwargs)
        self.source_fallback = source_fallback
        self.keep_existing = keep_existing

    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) and self.keep_existing or not self.get_source_value(model_instance):
            return super(AutoSlugField, self).pre_save(model_instance, add)

        value = self.get_slug_value(model_instance)
        if self.source_fallback and (value is None or value.strip() == ''):
            value = self.get_source_value(model_instance)
        setattr(model_instance, self.attname, value)
        return value

    def get_slug_value(self, model_instance):
        value = self.get_source_value(model_instance)
        return slugify(value)

    def get_source_value(self, model_instance):
        return getattr(model_instance, self.source_field)


class UniqueSlugField(AutoSlugField, models.SlugField):
    def __init__(self, source_field=None, keep_existing=False, *args, **kwargs):
        super(UniqueSlugField, self).__init__(source_field, *args, **kwargs)
        self.keep_existing = keep_existing

    def get_slug_value(self, model_instance):
        value = super(UniqueSlugField, self).get_slug_value(model_instance)
        filters = {
            self.attname + '__gte': value,
            self.attname + '__lte': value + '-9999'
        }
        last_instance = model_instance.__class__.objects.filter(**filters).order_by('-slug').first()
        if last_instance:
            if model_instance.pk and last_instance.pk == model_instance.pk:
                return value
            no = last_instance.slug.replace(value, "")
            try:
                value += "-" + str(abs(int(no)) + 1 if no else 1)
            except ValueError as ex:
                logging.warning("Could not increase counter", exc_info=ex)
        setattr(model_instance, self.attname, value)
        return value


class MarkDownField(SourceFieldMixin, models.TextField):
    def pre_save(self, model_instance, add):
        logging.debug(": %s", (model_instance, self.source_field))
        if not getattr(model_instance, self.source_field):
            return super(MarkDownField, self).pre_save(model_instance, add)

        value = getattr(model_instance, self.source_field)
        value = markdown(value)
        setattr(model_instance, self.attname, value)
        return value

    def to_python(self, value):
        value = super(MarkDownField, self).to_python(value)
        return mark_safe(value)

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)

    def contribute_to_class(self, cls, name, private_only=False, virtual_only=NOT_PROVIDED):
        super(MarkDownField, self).contribute_to_class(cls, name, private_only, virtual_only)
        if not self.source_field and name.endswith("_html"):
            self.source_field = name[:-5]


class JSONField(models.TextField):
    """Simple JSON field that stores python structures as JSON strings
    on database.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('default', '{}')
        super(JSONField, self).__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)

    def to_python(self, value):
        """
        Convert the input JSON value into python structures, raises
        django.core.exceptions.ValidationError if the data can't be converted.
        """
        if self.blank and not value:
            return {}
        value = value or '{}'
        if isinstance(value, six.binary_type):
            value = six.text_type(value, 'utf-8')
        if isinstance(value, six.string_types):
            try:
                # with django 1.6 i have '"{}"' as default value here
                if value[0] == value[-1] == '"':
                    value = value[1:-1]

                return json.loads(value)
            except Exception as err:
                raise ValidationError(str(err))
        else:
            return value

    def validate(self, value, model_instance):
        """Check value is a valid JSON string, raise ValidationError on
        error."""
        if isinstance(value, six.string_types):
            super(JSONField, self).validate(value, model_instance)
            try:
                json.loads(value)
            except Exception as err:
                raise ValidationError(str(err))

    def get_prep_value(self, value):
        """Convert value to JSON string before save"""
        try:
            return json.dumps(value)
        except Exception as err:
            raise ValidationError(str(err))

    def value_to_string(self, obj):
        """Return value from object converted to string properly"""
        value = getattr(obj, self.attname)
        return self.get_prep_value(value)

    def value_from_object(self, obj):
        value = getattr(obj, self.attname)
        return self.to_python(value)


class ChoicesIntEnum(IntEnum):
    """Extends IntEum with django choices generation capability"""

    @classmethod
    def choices(cls):
        return [(item.value, _(ChoicesIntEnum.capitalize(item))) for item in cls]

    @classmethod
    def capitalize(cls, item):
        name = item.name.replace("_", " ")
        return name[0].capitalize() + name[1:]

    @classmethod
    def values(cls):
        return [item.value for item in cls]


class BinaryMaskEnum(ChoicesIntEnum):
    # TODO: validate that values are actually a binary mask

    @classmethod
    def get_display(cls, value):
        return ", ".join((__(ChoicesIntEnum.capitalize(item)) for item in cls if item.value & value))
