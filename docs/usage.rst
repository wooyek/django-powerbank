=====
Usage
=====

To use Django Powerbank in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_powerbank.apps.DjangoPowerbankConfig',
        ...
    )

Add Django Powerbank's URL patterns:

.. code-block:: python

    from django_powerbank import urls as django_powerbank_urls


    urlpatterns = [
        ...
        url(r'^', include(django_powerbank_urls)),
        ...
    ]
