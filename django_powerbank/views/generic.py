# coding=utf-8
# Copyright 2015 Brave Labs sp. z o.o.
# All rights reserved.
#
# This source code and all resulting intermediate files are CONFIDENTIAL and
# PROPRIETY TRADE SECRETS of Brave Labs sp. z o.o.
# Use is subject to license terms. See NOTICE file of this project for details.
from django.views.generic.list import MultipleObjectMixin


class FilterMixin(MultipleObjectMixin):
    def get_queryset(self):
        qry = super().get_queryset()
        filter = self.request.GET.dict()
        filter.pop(self.page_kwarg, None)
        return qry.filter(**filter)
