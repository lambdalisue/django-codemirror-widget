# -*- coding: utf-8 -*-
#
# Created:    2010/09/09
# Author:         alisue
#
from django import forms
from django.conf import settings
from django.contrib.admin.widgets import AdminTextareaWidget
from django.template.loader import render_to_string
from django.utils import simplejson as json
from django.utils.safestring import mark_safe


# set default settings
CODEMIRROR_PATH = getattr(settings, 'CODEMIRROR_PATH', 'codemirror')
if CODEMIRROR_PATH.endswith('/'):
    CODEMIRROR_PATH = CODEMIRROR_PATH[:-1]
CODEMIRROR_DEFAULT_PARSERFILE = getattr(settings, 'CODEMIRROR_DEFAULT_PARSERFILE', 'parsedummy.js')
CODEMIRROR_DEFAULT_STYLESHEET = getattr(settings, 'CODEMIRROR_DEFAULT_STYLESHEET', '')


class CodeMirrorTextarea(forms.Textarea):
    u"""Textarea widget render with `CodeMirror`

    CodeMirror:
        http://codemirror.net/
    """

    class Media:
        css = {}
        js = (
            r"%s/js/codemirror.js" % CODEMIRROR_PATH,
        )

    def __init__(self, attrs=None, path=None, parserfile=None, stylesheet=None, **kwargs):
        u"""Constructor of CodeMirrorTextarea

        Attribute:
            path          - CodeMirror directory URI (DEFAULT = settings.CODEMIRROR_PATH)
            parserfile    - CodeMirror parserfile attribute (string or string array: DEFAULT = settings.CODEMIRROR_DEFAULT_PARSERFILE)
            stylesheet    - CodeMirror stylesheet attribute (uri or uri array: DEFAULT = settings.CODEMIRROR_DEFAULT_STYLESHEET)

        Example:
            *-------------------------------*
            + static
              + codemirror
                + css
                  - xmlcolors.css
                + js
                  - codemirror.js
                  - parsexml.js
            *-------------------------------*
            CODEMIRROR_PATH = r"codemirror"

            codemirror = CodeMirrorTextarea(
                # parserfile='parsexml.js',                                # Can be written as the left when only one file is needed.
                parserfile=['parsexml.js'],
                # stylesheet=r'xmlcolors.css'    # Can be written as the left when only one file is needed.
                stylesheet=[r'css/xmlcolors.css'],
            )
            document = forms.TextField(widget=codemirror)
        """
        super(CodeMirrorTextarea, self).__init__(attrs=attrs, **kwargs)
        self.path = path or settings.STATIC_URL + CODEMIRROR_PATH + '/js/'
        self.parserfile = parserfile or CODEMIRROR_DEFAULT_PARSERFILE
        self.stylesheet = stylesheet or CODEMIRROR_DEFAULT_STYLESHEET
        self.stylesheet = [settings.STATIC_URL + CODEMIRROR_PATH + '/' + css for css in self.stylesheet]
        if not hasattr(self.parserfile, '__iter__'):
            self.parserfile = (self.parserfile,)
        if not hasattr(self.stylesheet, '__iter__'):
            self.stylesheet = (self.stylesheet,)

    def render(self, name, value, attrs=None):
        u"""Render CodeMirrorTextarea"""
        html = super(CodeMirrorTextarea, self).render(name, value, attrs)
        kwargs = {
            'id': '"id_%s"' % name,
            'path': json.dumps(self.path),
            'parserfile': json.dumps(self.parserfile),
            'stylesheet': json.dumps(self.stylesheet),
        }
        for key in kwargs.keys():
            kwargs[key] = mark_safe(kwargs[key])
        code = render_to_string(r"codemirror/javascript.html", kwargs)
        body = "%s\n%s" % (html, code)
        return mark_safe(body)


class AdminCodeMirrorTextareaWidget(CodeMirrorTextarea, AdminTextareaWidget):
    u"""CodeMirrorTextarea for Admin site"""
    pass


class AdminHTMLEditor(AdminCodeMirrorTextareaWidget):
    def __init__(self, *args, **kwargs):
        kwargs['parserfile'] = ["parsexml.js", "parsecss.js", "tokenizejavascript.js", "parsejavascript.js", "parsehtmlmixed.js"]
        kwargs['stylesheet'] = ["css/xmlcolors.css", "css/jscolors.css", "css/csscolors.css"]
        super(AdminHTMLEditor, self).__init__(*args, **kwargs)
