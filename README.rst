=============================
Django Powerbank
=============================

.. image:: https://badge.fury.io/py/django-powerbank.svg
    :target: https://badge.fury.io/py/django-powerbank

.. image:: https://travis-ci.org/wooyek/django-powerbank.svg?branch=master
    :target: https://travis-ci.org/wooyek/django-powerbank

.. image:: https://codecov.io/gh/wooyek/django-powerbank/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/wooyek/django-powerbank

.. image:: https://readthedocs.org/projects/django-powerbank/badge/?version=latest
    :target: https://django-powerbank.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://pyup.io/repos/github/wooyek/django-powerbank/shield.svg
    :target: https://pyup.io/repos/github/wooyek/django-powerbank/
    :alt: Updates

Extra power for included batteries

A strongly opinionated collection of gems, stones, screws, duct tape & chewing gum that's helps me not to copy-paste code from project to project.


Documentation
-------------

The full documentation is at https://django-powerbank.readthedocs.io.

Quickstart
----------

Install Django Powerbank::

    pip install django-powerbank

Add it to your `INSTALLED_APPS`:

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

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
