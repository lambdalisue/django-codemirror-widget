django-codemirror-widget
=================================
.. image:: https://img.shields.io/pypi/v/django-codemirror-widget.svg
    :target: https://pypi.python.org/pypi/django-codemirror-widget/
    :alt: Version

.. image:: https://img.shields.io/pypi/status/django-codemirror-widget.svg
    :target: https://pypi.python.org/pypi/django-codemirror-widget/
    :alt: Status

.. image:: https://img.shields.io/pypi/l/django-codemirror-widget.svg
    :target: https://pypi.python.org/pypi/django-codemirror-widget/
    :alt: License

.. image:: https://img.shields.io/pypi/pyversions/django-codemirror-widget.svg
    :target: https://pypi.python.org/pypi/django-codemirror-widget/
    :alt: Python versions

`Django <https://www.djangoproject.com>`_ form widget library for using `CodeMirror <http://codemirror.net/>`_ on ``Textarea``.

Installation
-------------

.. code:: sh

    pip install django-codemirror-widget



Usage
-----------

1.  First, you need to specified ``CODEMIRROR_PATH`` on ``settings.py``.
    ``CODEMIRROR_PATH`` is the URI of CodeMirror directory like ``CODEMIRROR_PATH = r"javascript/codemirror"``.
    If you don't specify it, it defaults to ``'codemirror'``.
    CodeMirror should be put there.

2.  Use ``codemirror.CodeMirrorTextarea`` widget for target Textarea like below:

    .. code:: python

      from django import forms
      from codemirror import CodeMirrorTextarea
      
      codemirror_widget = CodeMirrorTextarea(
          mode="python",
          theme="cobalt",
          config={
              'fixedGutter': True
          },
      )
      document = forms.TextField(widget=codemirror_widget)


Settings
---------
Use the followings in your ``settings.py``.

``CODEMIRROR_PATH``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The URI of CodeMirror directory (your CodeMirror installation should live in ``{{ STATIC_URL }}/{{ CODEMIRROR_PATH }}``)

``CODEMIRROR_MODE``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The default mode which may be a string or configuration map (DEFAULT: ``'javascript'``)

``CODEMIRROR_THEME``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The default theme applied (DEFAULT: ``'default'``)

``CODEMIRROR_CONFIG``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Base mapping for the rest of the CodeMirror options (DEFAULT: ``{ 'lineNumbers': True }``)

``CODEMIRROR_JS_VAR_FORMAT``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A format string interpolated with the form field name to name a global JS variable that will hold the CodeMirror
editor object. For example with ``CODEMIRROR_JS_VAR_FORMAT = "%s_editor"`` and a field named 'code', the JS variable
name would be 'code_editor'. If ``CODEMIRROR_JS_VAR_FORMAT`` is None, no global variable is created (DEFAULT: None)
