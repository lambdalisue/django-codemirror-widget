# -*- coding: utf-8 -*-
#
# Created:    2010/09/09
# Author:         alisue
#
from django import forms
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.admin.widgets import AdminTextareaWidget
from django.utils.safestring import mark_safe
from django.core.exceptions import ImproperlyConfigured

# check is configured correctly
if not hasattr(settings, "CODEMIRROR_PATH"):
    raise ImproperlyConfigured("You must define the CODEMIRROR_PATH before using the CodeMirrorTextarea.")

if settings.CODEMIRROR_PATH.endswith('/'):
    settings.CODEMIRROR_PATH = settings.CODEMIRROR_PATH[:-1]
    
# set default settings
settings.CODEMIRROR_DEFAULT_PARSERFILE  = getattr(settings, 'CODEMIRROR_DEFAULT_PARSERFILE', 'parsedummy.js')
settings.CODEMIRROR_DEFAULT_STYLESHEET  = getattr(settings, 'CODEMIRROR_DEFAULT_STYLESHEET', '')

class CodeMirrorTextarea(forms.Textarea):
    u"""Textarea widget render with `CodeMirror`
    
    CodeMirror:
        http://codemirror.net/
    """

    class Media:
        css = {}
        js = (
            r"%s/codemirror.js" % settings.CODEMIRROR_PATH,
        )
        
    def __init__(self, attrs=None, path=None, parserfile=None, stylesheet=None, **kwargs):
        u"""Constructor of CodeMirrorTextarea
        
        Attribute:
            path          - CodeMirror directory URI (DEFAULT = settings.CODEMIRROR_PATH)
            parserfile    - CodeMirror parserfile attribute (string or string array: DEFAULT = settings.CODEMIRROR_DEFAULT_PARSERFILE)
            stylesheet    - CodeMirror stylesheet attribute (uri or uri array: DEFAULT = settings.CODEMIRROR_DEFAULT_STYLESHEET)
        
        Example:
            *-------------------------------*
            + javascript
              + codemirror
                + css
                  - xmlcolors.css
                + js
                  - codemirror.js
                  - parsexml.js
            *-------------------------------*
            settings.CODEMIRROR_PATH = r"javascript/codemirror/js"
            
            codemirror = CodeMirrorTextarea(
                # parserfile='parsexml.js',                                # Can be written as the left when only one file is needed.
                parserfile=['parsexml.js'],
                # stylesheet=r'javascript/codemirror/css/xmlcolors.css'    # Can be written as the left when only one file is needed.
                stylesheet=[r'javascript/codemirror/css/xmlcolors.css'],
            )
            document = forms.TextField(widget=codemirror)
        """
        super(CodeMirrorTextarea, self).__init__(attrs=attrs, **kwargs)
        self.path = path or settings.CODEMIRROR_PATH
        self.parserfile = parserfile or settings.CODEMIRROR_DEFAULT_PARSERFILE
        self.stylesheet = stylesheet or settings.CODEMIRROR_DEFAULT_STYLESHEET
        if not hasattr(self.parserfile, '__iter__'):
            self.parserfile = (self.parserfile,)
        if not hasattr(self.stylesheet, '__iter__'):
            self.stylesheet = (self.stylesheet,)
    
    def render(self, name, value, attrs=None):
        u"""Render CodeMirrorTextarea"""
        html = super(CodeMirrorTextarea, self).render(name, value, attrs)
        kwargs = {
            'name': name,
            'path': "%s%s/"%(settings.MEDIA_URL, self.path),
            'parserfile': "%s" % (", ".join(["\"%s\""%x for x in self.parserfile])),
            'stylesheet': "[%s]" % (", ".join(["\"%s%s\""%(settings.MEDIA_URL,x) for x in self.stylesheet])),
        }
        if self.stylesheet == []:
            kwargs['stylesheet'] = '""'
            
        code = render_to_string(r"codemirror/javascript.html", kwargs)
        body = "%s\n%s" % (html, code)
        return mark_safe(body)
    
class AdminCodeMirrorTextareaWidget(CodeMirrorTextarea, AdminTextareaWidget):
    u"""CodeMirrorTextarea for Admin site"""
    pass
