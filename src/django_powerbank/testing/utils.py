# coding=utf-8
from datetime import date, datetime


def model_to_request_data_dict(model):
    """
    Removes fields with None value. Test client will serialize them into 'None' strings that will cause validation errors.
    """
    from django.forms import model_to_dict
    data = model_to_dict(model)
    for k, v in data.copy().items():
        if v is None:
            del data[k]
        from django_powerbank.db.models.fields import ChoicesIntEnum
        if isinstance(v, ChoicesIntEnum):
            data[k] = int(v)
        if isinstance(v, date):
            data[k] = v.isoformat()
        if isinstance(v, datetime):
            data[k] = v.isoformat()
    return data
