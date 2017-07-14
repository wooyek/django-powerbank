# coding=utf-8
import logging
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseForbidden
from django.utils.translation import ugettext as __, ugettext_lazy as _

from . import ExceptionResponseView, Http403, Http302, ExceptionResponse


class AbstractAccessView(ExceptionResponseView):
    """Allows you to handle authorization before dispatch is called"""
    def check_authorization(self, *args, **kwargs):
        raise NotImplementedError()

    def dispatch(self, request, *args, **kwargs):
        try:
            return self.check_authorization() or super(AbstractAccessView, self).dispatch(request, *args, **kwargs)
        except ExceptionResponse as ex:
            logging.debug("ex.response: %s", ex.response)
            return ex.response


class AuthenticatedView(AbstractAccessView):
    """redirects unauthenticated users to login"""

    def check_authorization(self, *args, **kwargs):
        if not self.is_authenticated(*args, **kwargs):
            return self.handle_anonymous(*args, **kwargs)

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def is_authenticated(self, *args, **kwargs):
        return self.request.user.is_authenticated()

    # noinspection PyUnusedLocal
    def handle_anonymous(self, *args, **kwargs):
        path = self.request.get_full_path()
        return redirect_to_login(path)

# Backward compatibility alias
AccessMixin = AuthenticatedView


class AbstractAuthorizedView(AuthenticatedView):
    forbidden_message = _("You are not authorized to view this page")

    def is_authorized(self, *args, **kwargs):
        raise NotImplementedError()

    def get_forbidden_message(self):
        return self.forbidden_message

    def handle_forbidden(self):
        return HttpResponseForbidden(self.get_forbidden_message())

    def check_authorization(self, *args, **kwargs):
        if not self.request.user.is_authenticated(*args, **kwargs):
            return self.handle_anonymous(*args, **kwargs)

        if not self.is_authorized(*args, **kwargs):
            return self.handle_forbidden()


class StaffRequiredMixin(AbstractAuthorizedView):
    def is_authorized(self, *args, **kwargs):
        return self.request.user.is_staff
