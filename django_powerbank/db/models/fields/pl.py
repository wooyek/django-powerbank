# coding=utf-8
# Copyright 2015 Brave Labs sp. z o.o.
# All rights reserved.
#
# This source code and all resulting intermediate files are CONFIDENTIAL and
# PROPRIETY TRADE SECRETS of Brave Labs sp. z o.o.
# Use is subject to license terms. See NOTICE file of this project for details.
from django.db import models
from localflavor.pl import forms
from django.utils.translation import ugettext as __, ugettext_lazy as _


class PlRegonField(models.CharField):
    def __init__(self, *args, **kwargs):
        verbose_name = kwargs.pop('verbose_name', _("numer identyfikacyjny REGON"))
        max_length = kwargs.pop('max_length', 14)
        super().__init__(verbose_name=verbose_name, max_length=max_length, *args, **kwargs)

    def formfield(self, **kwargs):
        return super().formfield(form_class=forms.PLREGONField, **kwargs)


class PlNipField(models.CharField):
    def __init__(self, *args, **kwargs):
        verbose_name = kwargs.pop('verbose_name', _("numer identyfikacji podatkowej"))
        max_length = kwargs.pop('max_length', 13)
        super().__init__(verbose_name=verbose_name, max_length=max_length, *args, **kwargs)

    def formfield(self, **kwargs):
        return super().formfield(form_class=forms.PLNIPField, **kwargs)
