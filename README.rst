Django form widget library for using `CodeMirror <http://codemirror.net/>`_ on Textarea


Install
===========================================

	sudo pip install django-codemirror-widget

or

    sudo pip install git+git://github.com/lambdalisue/django-codemirror-widget.git#egg=django-code-mirror


How to Use
==========================================

1.	First, you need to specified ``CODEMIRROR_PATH`` on ``settings.py``.
	``CODEMIRROR_PATH`` is the URI of CodeMirror directory like ``CODEMIRROR_PATH = r"javascript/codemirror"``.
	If you don't specify it, it defaults to ``'codemirror'``.
	CodeMirror should be put there.
2.	Use ``codemirror.widgets.CodeMirrorTextarea`` widgets for target Textarea like below::
	
		from django import forms
		from codemirror.widgets import CodeMirrorTextarea

		codemirror = CodeMirrorTextarea(mode="python", theme="cobalt", config={ 'fixedGutter': True })
		document = forms.TextField(widget=codemirror)


Settings
=========================================

``CODEMIRROR_PATH``
    the URI of CodeMirror directory (your CodeMirror installation should live in ``{{ STATIC_URL }}/{{ CODEMIRROR_PATH }}``)

``CODEMIRROR_MODE``
	the default mode which may be a string or configuration map (DEFAULT: 'javascript')

``CODEMIRROR_THEME``
    the default theme applied (DEFAULT: 'default')

``CODEMIRROR_CONFIG``
    base mapping for the rest of the CodeMirror options (DEFAULT: ``{ 'lineNumbers': True }``)

``CODEMIRROR_JS_VAR_FORMAT``
    A format string interpolated with the form field name to name a global JS variable that will hold the CodeMirror
    editor object. For example with ``CODEMIRROR_JS_VAR_FORMAT = "%s_editor"`` and a field named 'code', the JS variable
    name would be 'code_editor'. If ``CODEMIRROR_JS_VAR_FORMAT`` is None, no global variable is created (DEFAULT: None)
