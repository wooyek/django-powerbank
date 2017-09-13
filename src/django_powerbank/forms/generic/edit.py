# coding=utf-8
from django.views.generic.edit import FormMixin


# class MultiFormMixin(FormMixin):
#     def get_form_kwargs(self, prefix=None):
#         """
#         Returns the keyword arguments for instantiating the form.
#         """
#         kwargs = {
#             'initial': self.get_initial(prefix),
#             'prefix': prefix or self.get_prefix(),
#         }
#
#         # noinspection PyUnresolvedReferences
#         request = self.request
#         if request.method in ('POST', 'PUT'):
#             kwargs.update({
#                 'data': request.POST,
#                 'files': request.FILES,
#             })
#         return kwargs
#
#     def get_initial(self, prefix=None):
#         """
#         Returns the initial data to use for forms on this view.
#         """
#         return self.initial.setdefault(prefix, {}).copy()
#
#     def get_form(self, form_class=None, prefix=None):
#         """
#         Returns an instance of the form to be used in this view.
#         """
#         if form_class is None:
#             form_class = self.get_form_class(prefix)
#         return form_class(**self.get_form_kwargs(prefix))
#
#     def get_form_class(self, prefix=None):
#         """
#         Returns the form class to use in this view
#         """
#         return self.form_class[prefix]
#
#     def post(self, request, *args, **kwargs):
#         # noinspection PyUnresolvedReferences
#         form_set = self.get_form_set()
#         if all((f.is_valid() for f in form_set)):
#             return self.form_valid(form_set)
#         else:
#             return self.form_invalid(form_set)
