import six
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.http.response import HttpResponseRedirectBase, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import redirect
from django.views import View


class ExceptionResponse(Exception):
    """
    Generic exception for signalling that instead of default error handling
    we should use attached response
    """

    def __init__(self, response):
        self.response = response


class Http403(PermissionDenied, ExceptionResponse):
    """
    A convenience wrapper around :py:class:~django.core.exceptions.PermissionDenied`
    """

    def __init__(self, response):
        if response is None:
            response = HttpResponseForbidden()
        elif not isinstance(response, HttpResponse):
            response = HttpResponseForbidden(response)
        super(Http403, self).__init__(response)


class Http302(ExceptionResponse):
    """Wraps a redirect shortcut call into the ResponseException"""

    def __init__(self, to, *args, **kwargs):
        if isinstance(to, HttpResponseRedirectBase):
            response = to
        else:
            response = redirect(to, *args, **kwargs)
        super(Http302, self).__init__(response)


class Http400(ExceptionResponse):
    def __init__(self, response):
        if isinstance(response, six.string_types):
            response = HttpResponseBadRequest(response)
        super(Http400, self).__init__(response)


class Http401(ExceptionResponse):
    def __init__(self, response):
        if isinstance(response, six.string_types):
            response = HttpResponseNotFound(response)
        super(Http401, self).__init__(response)


class ExceptionResponseView(View):
    def dispatch(self, request, *args, **kwargs):
        try:
            return super(ExceptionResponseView, self).dispatch(request, *args, **kwargs)
        except ExceptionResponse as ex:
            return ex.response
