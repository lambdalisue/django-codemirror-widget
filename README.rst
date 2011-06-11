Django form widget library for using `CodeMirror <http://codemirror.net/>`_ on Textarea


Install
===========================================

	sudo pip install django-codemirror-widget

or

    sudo pip install git+git://github.com/lambdalisue/django-codemirror-widget.git#egg=django-code-mirror


How to Use
==========================================

1.	First, you need to specified ``CODEMIRROR_PATH`` on ``settings.py``
	``CODEMIRROR_PATH`` is the URI of CodeMirror directory like ``CODEMIRROR_PATH = r"javascript/codemirror"``
2.	Use ``codemirror.widgets.CodeMirrorTextarea`` widgets for target Textarea like below::
	
		from django import forms
		from codemirror.widgets import CodeMirrorTextarea

		codemirror = CodeMirrorTextarea(
			parserfile=['parsexml.js'],
			stylesheet=[r'javascript/codemirror/css/xmlcolor.css'],
		)
		document = forms.TextField(widget=codemirror)

Settings
=========================================
``CODEMIRROR_PATH``
    the URI of CodeMirror directory

``CODEMIRROR_DEFAULT_PARSER``
	the default parser (DEFAULT: 'parsedummy.js')

``CODEMIRROR_DEFAULT_STYLESHEET``
	the default stylesheet (DEFAULT: '')
