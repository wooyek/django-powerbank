#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
import uuid

from pip.req import parse_requirements

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

install_requires = parse_requirements(
    os.path.join(os.path.dirname(__file__), "requirements", "production.txt"),
    session=uuid.uuid1()
)

test_requirements = parse_requirements(
    os.path.join(os.path.dirname(__file__), "requirements", "test.txt"),
    session=uuid.uuid1()
)


def get_version(*file_paths):
    """Retrieves the version from django_powerbank/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version("django_powerbank", "__init__.py")

if sys.argv[-1] == 'publish':
    try:
        import wheel

        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'bump':
    print("Tagging the version on git:")
    os.system("bumpversion patch --no-tag")
    sys.exit()

setup(
    name='django-powerbank',
    version=version,
    description="Extra utilities currently missing from Django",
    long_description=readme + '\n\n' + history,
    author="Janusz Skonieczny",
    author_email='js+pypi@bravelabs.pl',
    url='https://github.com/wooyek/django_powerbank',
    packages=find_packages(),
    # package_dir={
    #     'django_powerbank': 'django_powerbank'
    # },
    entry_points={
        'console_scripts': [
            'django_powerbank=django_powerbank.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=[str(r.req) for r in install_requires],
    license="MIT license",
    zip_safe=False,
    keywords='django_powerbank',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=[str(r.req) for r in test_requirements]
)
