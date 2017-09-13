# coding=utf-8
import six
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from six import python_2_unicode_compatible
from django.utils.translation import ugettext as __, ugettext_lazy as _


@python_2_unicode_compatible
class BaseModel(models.Model):
    class Meta:
        abstract = True

    def __str__(self):
        return "{}:{}".format(self.__class__.__name__, self.pk)

    def __repr__(self):
        from django.utils.encoding import force_str
        fields = ", ".join(("{}={}".format(k, repr(v)) for k, v in self.to_dict().items() if v is not None))
        return force_str('{}({})'.format(self.__class__.__name__, fields))

    def get_field_name(self, field_name):
        try:
            return self._meta.get_field(field_name).verbose_name.capitalize()
        except FieldDoesNotExist:
            name = field_name.replace('_', ' ')
            return _(name).capitalize()

    def to_dict(self, include=None, exclude=None):
        """
        Return a dict containing the entity's property values.

        Args:
          include: Optional set of property names to include, default all.
          exclude: Optional set of property names to skip, default none.
            A name contained in both include and exclude is excluded.
        """
        if (include is not None and
                not isinstance(include, (list, tuple, set, frozenset))):
            raise TypeError('include should be a list, tuple or set')
        if (exclude is not None and
                not isinstance(exclude, (list, tuple, set, frozenset))):
            raise TypeError('exclude should be a list, tuple or set')
        values = self.__dict__.copy()
        # noinspection PyProtectedMember
        # field_names = [f.name for f in self._meta._get_fields(reverse=False)]
        for name in list(values.keys()):
            if include is not None and name not in include:
                values.pop(name)
            if exclude is not None and name in exclude:
                values.pop(name)
            if name.startswith("_"):
                values.pop(name, None)
        return values

    def get_field_names(self):
        return [f.name for f in self._meta.get_fields()]

    def populate(self, **kwargs):
        """
        Populate an instance from keyword arguments.

        Each keyword argument will be used to set a corresponding
        field.  Keywords must refer to valid property name.  This is
        similar to passing keyword arguments to the Model constructor.
        """
        cls = self.__class__
        for name, value in kwargs.items():
            prop = getattr(cls, name)  # Raises AttributeError for unknown properties.
            if not hasattr(prop, "__get__"):
                raise TypeError('Cannot set non-field {} ({})'.format(name, type(prop)))
            # prop._set_value(self, value)
            setattr(self, name, value)
