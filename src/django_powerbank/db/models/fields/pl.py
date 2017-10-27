# coding=utf-8
from django.db import models
from localflavor.pl import forms
from django.utils.translation import ugettext as __, ugettext_lazy as _


class PlRegonField(models.CharField):
    def __init__(self, *args, **kwargs):
        verbose_name = kwargs.pop('verbose_name', _("numer identyfikacyjny REGON"))
        max_length = kwargs.pop('max_length', 14)
        super(PlRegonField, self).__init__(verbose_name=verbose_name, max_length=max_length, *args, **kwargs)

    def formfield(self, **kwargs):
        return super(PlRegonField, self).formfield(form_class=forms.PLREGONField, **kwargs)

    def to_python(self, value):
        return super(PlRegonField, self).to_python(value) or None


class PlNipField(models.CharField):
    def __init__(self, *args, **kwargs):
        verbose_name = kwargs.pop('verbose_name', _("numer identyfikacji podatkowej"))
        max_length = kwargs.pop('max_length', 13)
        super(PlNipField, self).__init__(verbose_name=verbose_name, max_length=max_length, *args, **kwargs)

    def formfield(self, **kwargs):
        return super(PlNipField, self).formfield(form_class=forms.PLNIPField, **kwargs)

    def to_python(self, value):
        return super(PlNipField, self).to_python(value) or None

