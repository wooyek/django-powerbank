# coding=utf-8
from django.views.generic.list import MultipleObjectMixin


class FilterMixin(MultipleObjectMixin):
    def get_queryset(self):
        qry = super().get_queryset()
        filter = self.request.GET.dict()
        filter.pop(self.page_kwarg, None)
        return qry.filter(**filter)
