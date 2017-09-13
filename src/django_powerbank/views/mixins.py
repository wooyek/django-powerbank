# coding=utf-8
import logging

from django.http import HttpResponseRedirect
from django.views.generic.base import ContextMixin, View


class ReturnUrlMx(ContextMixin, View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.return_url = None

    def get_context_data(self, **kwargs):
        return_url = kwargs.pop("return_url", self.return_url)
        logging.debug("return_url: %s" % return_url)
        if not return_url:
            try:
                # A hail mary hack, to provide a sensible return_url when
                # this request is not referred to
                return_url = self.get_success_url()
            except:
                pass
        return super().get_context_data(return_url=return_url, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        """
        Does request processing for return_url query parameter and redirects with it's missing

        We can't do that in the get method, as it does not exist in the View base class
        and child mixins implementing get do not call super().get
        """

        self.return_url = request.GET.get('return_url', None)
        referrer = request.META.get('HTTP_REFERER', None)

        # leave alone POST and ajax requests and if return_url is explicitly left empty
        if request.method != "GET" or \
                request.is_ajax() or \
                self.return_url or \
                referrer is None or \
                self.return_url is None and 'return_url' in request.GET:
            return super().dispatch(request, *args, **kwargs)

        if not self.return_url:
            url = request.get_full_path()
            if url.find("?") < 0:
                url = "?return_url=".join((url, referrer))
            else:
                url = "&return_url=".join((url, referrer))
            return HttpResponseRedirect(url)

    def get_success_url(self):
        return self.return_url
