# -*- coding: utf-8 -*-
#
# Created:    2010/09/09
# Author:         alisue
#
import json
from django import forms
from django.conf import settings
from django.contrib.admin.widgets import AdminTextareaWidget
from django.utils.safestring import mark_safe

# set default settings
CODEMIRROR_PATH = getattr(settings, 'CODEMIRROR_PATH', 'codemirror')
if CODEMIRROR_PATH.endswith('/'):
    CODEMIRROR_PATH = CODEMIRROR_PATH[:-1]
CODEMIRROR_MODE = getattr(settings, 'CODEMIRROR_MODE', 'javascript')

class CodeMirrorTextarea(forms.Textarea):
    u"""Textarea widget render with `CodeMirror`

    CodeMirror:
        http://codemirror.net/
    """
    
    @property
    def media(self):
        mode_name = self.mode['name']
        return forms.Media(css = {
                'all': ("%s/lib/codemirror.css" % CODEMIRROR_PATH,),
            },
            js = (
                "%s/lib/codemirror.js" % CODEMIRROR_PATH,
                "%s/mode/%s/%s.js" % (CODEMIRROR_PATH, mode_name, mode_name),
            ))
    
    def __init__(self, attrs=None, mode=None, **kwargs):
        u"""Constructor of CodeMirrorTextarea

        Attribute:
            path          - CodeMirror directory URI (DEFAULT = settings.CODEMIRROR_PATH)
            mode          - Name of language or a configuration object as described in CodeMirror docs (DEFAULT = settings.CODEMIRROR_MODE)

        Example:
            *-------------------------------*
            + static
              + codemirror
                + lib
                  - codemirror.js
                + mode
                  + python
                    - python.js
            *-------------------------------*
            CODEMIRROR_PATH = r"codemirror"

            codemirror = CodeMirrorTextarea(mode="python")
            document = forms.TextField(widget=codemirror)
        """
        super(CodeMirrorTextarea, self).__init__(attrs=attrs, **kwargs)
        mode = mode or CODEMIRROR_MODE
        if isinstance(mode, basestring):
            mode = { 'name': mode }
        self.mode = mode
    
    def render(self, name, value, attrs=None):
        u"""Render CodeMirrorTextarea"""
        output = [super(CodeMirrorTextarea, self).render(name, value, attrs),
            '<script type="text/javascript">CodeMirror.fromTextArea(document.getElementById(%s), { mode: %s });</script>' % ('"id_%s"' % name, json.dumps(self.mode))]
        return mark_safe('\n'.join(output))

