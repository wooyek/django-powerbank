# coding=utf-8
import logging
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseForbidden
from django.utils.translation import ugettext as __, ugettext_lazy as _

from . import ExceptionResponseView, Http403, Http302, ExceptionResponse


class AccessMixin(ExceptionResponseView):
    forbidden_message = _("You are not authorized to view this page")

    def is_authorized(self, *args, **kwargs):
        return self.request.user.is_authenticated()

    def get_forbidden_message(self):
        return self.forbidden_message

    def check_authorization(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            path = self.request.get_full_path()
            return redirect_to_login(path)

        if not self.is_authorized(*args, **kwargs):
            return self.handle_forbidden()

    def handle_forbidden(self):
        return HttpResponseForbidden(self.get_forbidden_message())

    def dispatch(self, request, *args, **kwargs):
        try:
            return self.check_authorization() or super().dispatch(request, *args, **kwargs)
        except ExceptionResponse as ex:
            logging.debug("ex.response: %s", ex.response)
            return ex.response


class StaffRequiredMixin(AccessMixin):
    def is_authorized(self, *args, **kwargs):
        return self.request.user.is_staff
