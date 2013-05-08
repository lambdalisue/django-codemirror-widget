# -*- coding: utf-8 -*-
#
# Created:    2010/09/09
# Author:         alisue
#
import json, re
from itertools import chain
from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe

# set default settings
CODEMIRROR_PATH = getattr(settings, 'CODEMIRROR_PATH', 'codemirror')
if CODEMIRROR_PATH.endswith('/'):
    CODEMIRROR_PATH = CODEMIRROR_PATH[:-1]
CODEMIRROR_MODE = getattr(settings, 'CODEMIRROR_MODE', 'javascript')
CODEMIRROR_THEME = getattr(settings, 'CODEMIRROR_THEME', 'default')
CODEMIRROR_CONFIG = getattr(settings, 'CODEMIRROR_CONFIG', { 'lineNumbers': True })

THEME_CSS_FILENAME_RE = re.compile(r'[\w-]+')

def isstring(obj):
    try:
        return isinstance(obj, basestring)
    except NameError:
        return isinstance(obj, str)

class CodeMirrorTextarea(forms.Textarea):
    """Textarea widget render with `CodeMirror`

    CodeMirror:
        http://codemirror.net/
    """
    
    @property
    def media(self):
        mode_name = self.mode_name
        return forms.Media(css = {
                'all': ("%s/lib/codemirror.css" % CODEMIRROR_PATH,) +
                    tuple("%s/theme/%s.css" % (CODEMIRROR_PATH, theme_css_filename)
                        for theme_css_filename in self.theme_css),
            },
            js = (
                "%s/lib/codemirror.js" % CODEMIRROR_PATH,
                "%s/mode/%s/%s.js" % (CODEMIRROR_PATH, mode_name, mode_name),
            ) + tuple(
                "%s/mode/%s/%s.js" % (CODEMIRROR_PATH, dependency, dependency)
                    for dependency in self.dependencies)
            )
    
<<<<<<< HEAD
    def __init__(self, attrs=None, mode=None, theme=None, config=None, dependencies=(), **kwargs):
        u"""Constructor of CodeMirrorTextarea
=======
    def __init__(self, attrs=None, mode=None, theme=None, config=None, **kwargs):
        """Constructor of CodeMirrorTextarea
>>>>>>> d3130cbe429c6489cc47e8a6f732cf944d948687

        Attribute:
            path          - CodeMirror directory URI (DEFAULT = settings.CODEMIRROR_PATH)
            mode          - Name of language or a modal configuration object as described in CodeMirror docs.
                            Used to autoload an appropriate language plugin js file according to filename conventions.
                            (DEFAULT = settings.CODEMIRROR_MODE)
            theme         - Name of theme. Also autoloads theme plugin css according to filename conventions.
                            (DEFAULT = settings.CODEMIRROR_THEME)
            config        - The rest of the options passed into CodeMirror as a python map.
                            (updated from settings.CODEMIRROR_CONFIG)

        Example:
            *-------------------------------*
            + static
              + codemirror
                + lib
                  - codemirror.js
                  - codemirror.css
                + mode
                  + python
                    - python.js
                + theme
                  + cobalt.css
            *-------------------------------*
            CODEMIRROR_PATH = "codemirror"

            codemirror = CodeMirrorTextarea(mode="python", theme="cobalt", config={ 'fixedGutter': True })
            document = forms.TextField(widget=codemirror)
        """
        super(CodeMirrorTextarea, self).__init__(attrs=attrs, **kwargs)
        
        mode = mode or CODEMIRROR_MODE
<<<<<<< HEAD
        if isstring(mode):
=======
        if isinstance(mode, str):
>>>>>>> d3130cbe429c6489cc47e8a6f732cf944d948687
            mode = { 'name': mode }
        self.mode_name = mode['name']
        self.dependencies = dependencies
        
        theme = theme or CODEMIRROR_THEME
        theme_css_filename = THEME_CSS_FILENAME_RE.search(theme).group(0)
        if theme_css_filename == 'default':
            self.theme_css = []
        else:
            self.theme_css = [theme_css_filename]
        
        config = config or {}
        self.option_json = json.dumps(dict(chain(
            CODEMIRROR_CONFIG.items(),
            config.items(),
            [('mode', mode), ('theme', theme)])))
    
    def render(self, name, value, attrs=None):
        """Render CodeMirrorTextarea"""
        output = [super(CodeMirrorTextarea, self).render(name, value, attrs),
            '<script type="text/javascript">CodeMirror.fromTextArea(document.getElementById(%s), %s);</script>' %
                ('"id_%s"' % name, self.option_json)]
        return mark_safe('\n'.join(output))

