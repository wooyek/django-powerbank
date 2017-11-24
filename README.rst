================
Django Powerbank
================


.. image:: https://img.shields.io/pypi/v/django-powerbank.svg
        :target: https://pypi.python.org/pypi/django-powerbank

.. image:: https://img.shields.io/travis/wooyek/django-powerbank.svg
        :target: https://travis-ci.org/wooyek/django-powerbank

.. image:: https://readthedocs.org/projects/django-powerbank/badge/?version=latest
        :target: https://django-powerbank.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status
.. image:: https://coveralls.io/repos/github/wooyek/django-powerbank/badge.svg?branch=develop
        :target: https://coveralls.io/github/wooyek/django-powerbank?branch=develop
        :alt: Coveralls.io coverage

.. image:: https://codecov.io/gh/wooyek/django-powerbank/branch/develop/graph/badge.svg
        :target: https://codecov.io/gh/wooyek/django-powerbank
        :alt: CodeCov coverage

.. image:: https://api.codeclimate.com/v1/badges/0e7992f6259bc7fd1a1a/maintainability
        :target: https://codeclimate.com/github/wooyek/django-powerbank/maintainability
        :alt: Maintainability

.. image:: https://img.shields.io/github/license/wooyek/django-powerbank.svg
        :target: https://github.com/wooyek/django-powerbank/blob/develop/LICENSE
        :alt: License

.. image:: https://img.shields.io/twitter/url/https/github.com/wooyek/django-powerbank.svg?style=social
        :target: https://twitter.com/intent/tweet?text=Wow:&url=https://github.com/wooyek/django-powerbank
        :alt: Tweet about this project

.. image:: https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg
        :target: https://saythanks.io/to/wooyek

Extra power for included batteries

* Free software: MIT license
* Documentation: https://django-powerbank.readthedocs.io.

Work in progress
----------------

This package was created with `wooyek/cookiecutter-django-app`_ project template.
It may fool you by having a lot of cookie filling just ready from the start.
Be warned! It may not be ready for eating!

.. image:: https://media.giphy.com/media/DmLUhoNUBfz5C/giphy.gif

Features
--------

* Pending :D

Demo
----

To run an example project for this django reusable app, click the button below and start a demo serwer on Heroku

.. image:: https://www.herokucdn.com/deploy/button.png
    :target: https://heroku.com/deploy
    :alt: Deploy Django Opt-out example project to Heroku


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


Running Tests
-------------

Does the code actually work?

::
    $ pipenv install --dev
    $ pipenv shell
    $ tox


We recommend using pipenv_ but a legacy approach to creating virtualenv and installing requirements should also work.
Please install `requirements/development.txt` to setup virtual env for testing and development.


Credits
-------

This package was created with Cookiecutter_ and the `wooyek/cookiecutter-django-app`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`wooyek/cookiecutter-django-app`: https://github.com/wooyek/cookiecutter-django-app
.. _`pipenv`: https://docs.pipenv.org/install.html#fancy-installation-of-pipenv
