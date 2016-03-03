# -*- coding: utf-8 -*-
#
# Created:    2010/09/09
# Author:         alisue
#
from itertools import chain
import re

from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe

from codemirror import utils


# set default settings
CODEMIRROR_PATH = getattr(settings, 'CODEMIRROR_PATH', 'codemirror')
if CODEMIRROR_PATH.endswith('/'):
    CODEMIRROR_PATH = CODEMIRROR_PATH[:-1]
CODEMIRROR_MODE = getattr(settings, 'CODEMIRROR_MODE', 'javascript')
CODEMIRROR_THEME = getattr(settings, 'CODEMIRROR_THEME', 'default')
CODEMIRROR_CONFIG = getattr(settings, 'CODEMIRROR_CONFIG', { 'lineNumbers': True })
CODEMIRROR_JS_VAR_FORMAT = getattr(settings, 'CODEMIRROR_JS_VAR_FORMAT', None)

THEME_CSS_FILENAME_RE = re.compile(r'[\w-]+')


class CodeMirrorTextarea(forms.Textarea):
    u"""Textarea widget render with `CodeMirror`

    CodeMirror:
        http://codemirror.net/
    """

    @property
    def media(self):
        mode_name = self.mode_name
        js = ["%s/lib/codemirror.js" % CODEMIRROR_PATH]

        if not self.custom_mode:
            js.append("%s/mode/%s/%s.js" % (CODEMIRROR_PATH, mode_name, mode_name))

        js.extend(
            "%s/mode/%s/%s.js" % (CODEMIRROR_PATH, dependency, dependency)
                for dependency in self.dependencies)
        js.extend("%s/addon/%s.js" % (CODEMIRROR_PATH, addon) for addon in self.addon_js)

        if self.keymap:
            js.append("%s/keymap/%s.js" % (CODEMIRROR_PATH, self.keymap))

        if self.custom_js:
            js.extend(self.custom_js)

        css = ["%s/lib/codemirror.css" % CODEMIRROR_PATH]
        css.extend(
            "%s/theme/%s.css" % (CODEMIRROR_PATH, theme_css_filename)
                for theme_css_filename in self.theme_css)
        css.extend(
            "%s/addon/%s.css" % (CODEMIRROR_PATH, css_file)
                for css_file in self.addon_css)

        if self.custom_css:
            css.extend(self.custom_css)

        return forms.Media(
            css={
                'all': css
            },
            js=js
        )

    def __init__(
            self, attrs=None, mode=None, theme=None, config=None, dependencies=(),
            js_var_format=None, addon_js=(), addon_css=(), custom_mode=None, custom_js=(),
            keymap=None, custom_css=None, **kwargs):
        u"""Constructor of CodeMirrorTextarea

        Attribute:
            path          - CodeMirror directory URI (DEFAULT = settings.CODEMIRROR_PATH)
            mode          - Name of language or a modal configuration object as described in CodeMirror docs.
                            Used to autoload an appropriate language plugin js file according to filename conventions.
                            (DEFAULT = settings.CODEMIRROR_MODE)
            theme         - Name of theme. Also autoloads theme plugin css according to filename conventions.
                            (DEFAULT = settings.CODEMIRROR_THEME)
            config        - The rest of the options passed into CodeMirror as a python map.
                            (updated from settings.CODEMIRROR_CONFIG)
            dependencies  - Some modes depend on others, you can pass extra modes dependencies with this argument.
                            For example for mode="htmlmixed", you must pass dependencies=("xml", "javascript", "css").
            js_var_format - A format string interpolated with the form field name to name a global JS variable that will
                            hold the CodeMirror editor object. For example with js_var_format="%s_editor" and a field
                            named "code", the JS variable name would be "code_editor". If None is passed, no global
                            variable is created (DEFAULT = settings.CODEMIRROR_JS_VAR_FORMAT)
            addon_js      - Various addons are available for CodeMirror. You can pass the names of any addons to load
                            with this argument. For example, for mode="django", you must pass addon_js=("mode/overlay", ).
            addon_css     - Some addons require corresponding CSS files. Since not every addon requires a CSS file, and
                            the names of these files do not always follow a convention, they must be listed separately.
                            For example, addon_css=("display/fullscreen", ).
            custom_mode   - To use a custom mode (i.e. one not included in the standard CodeMirror distribution), set this to
                            the name, or configuration object, of the mode, and ensure "mode" is None. For example,
                            custom_mode="my_custom_mode".
            custom_js     - To include other Javascript files with this widget that are not defined in the CodeMirror package,
                            set this to a list of pathnames. If "custom_mode" is defined, this will probably contain the path
                            of the file defining that mode. Paths in this list will not be prepended with settings.CODEMIRROR_PATH.
                            For example, custom_js=("site_js/my_custom_mode.js", )
            keymap        - The name of a keymap to use. Keymaps are located in settings.CODEMIRROR_PATH/keymap. Default: None.
            custom_css    - To include other CSS files with this widget that are not defined in the CodeMirror package,
                            set this to a list of pathnames. Paths in this list will not be prepended with any path.
                            For example, custom_css=("site_css/my_styles.css", )

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
                + addon
                  + display
                    - fullscreen.js
                    - fullscreen.css
              + site_js
                - my_custom_mode.js
            *-------------------------------*
            CODEMIRROR_PATH = "codemirror"

            codemirror = CodeMirrorTextarea(mode="python", theme="cobalt", config={ 'fixedGutter': True })
            document = forms.TextField(widget=codemirror)
        """
        super(CodeMirrorTextarea, self).__init__(attrs=attrs, **kwargs)

        mode = mode or custom_mode or CODEMIRROR_MODE
        if utils.isstring(mode):
            mode = { 'name': mode }
        self.mode_name = mode['name']
        self.custom_mode = custom_mode
        self.dependencies = dependencies
        self.addon_js = addon_js
        self.addon_css = addon_css
        self.custom_js = custom_js
        self.custom_css = custom_css
        self.keymap = keymap
        self.js_var_format = js_var_format or CODEMIRROR_JS_VAR_FORMAT

        theme = theme or CODEMIRROR_THEME
        theme_css_filename = THEME_CSS_FILENAME_RE.search(theme).group(0)
        if theme_css_filename == 'default':
            self.theme_css = []
        else:
            self.theme_css = [theme_css_filename]

        config = config or {}
        self.option_json = utils.CodeMirrorJSONEncoder().encode(dict(chain(
            CODEMIRROR_CONFIG.items(),
            config.items(),
            [('mode', mode), ('theme', theme)])))

    def render(self, name, value, attrs=None):
        u"""Render CodeMirrorTextarea"""
        if self.js_var_format is not None:
            js_var_bit = 'var %s = ' % (self.js_var_format % name)
        else:
            js_var_bit = ''
        output = [super(CodeMirrorTextarea, self).render(name, value, attrs),
            '<script type="text/javascript">%sCodeMirror.fromTextArea(document.getElementById(%s), %s);</script>' %
                (js_var_bit, '"id_%s"' % name, self.option_json)]
        return mark_safe('\n'.join(output))
