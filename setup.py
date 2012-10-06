#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:       Alisue
# Last Change:  18-Mar-2011.
#
from setuptools import setup, find_packages

version = "0.2.0"

def read(filename):
    import os.path
    return open(os.path.join(os.path.dirname(__file__), filename)).read()
setup(
    name="django-codemirror-widget",
    version=version,
    description = "django-codemirror-widget is Django form widget library for using CodeMirror on textarea",
    long_description=read('README.rst'),
    classifiers = [
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    keywords = "django widget textarea codemirror",
    author = "Alisue",
    author_email = "lambdalisue@hashnote.net",
    url=r"https://github.com/lambdalisue/django-codemirror-widget",
    download_url = r"https://github.com/lambdalisue/django-codemirror-widget/tarball/master",
    license = 'BSD',
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    install_requires=['setuptools'],
)
