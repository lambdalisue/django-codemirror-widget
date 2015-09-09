# -*- coding: utf-8 -*-
"""
Common utilities for codemirror module.
"""

import hashlib
import json


def isstring(obj):
    try:
        return isinstance(obj, basestring)
    except NameError:
        return isinstance(obj, str)


class CodeMirrorJavascript(object):
    """An object used to mark Javascript sections in JSON output.

    If an object of this type is passed to CodeMirrorJSONEncoder().encode(), the text
    containined in it will be output with no transformations applied. Most likely this
    will not be valid JSON, but it will be valid Javascript, assuming valid Javascript
    was passed to the constructor.

    Example usage:

    my_data = {
        'someKey': True,
        'someCallback': CodeMirrorJavascript("function() { return true; }")
    }

    CodeMirrorJSONEncoder().encode(my_data)

    # -> '{"someKey": true, "someCallback": function() { return true; }}'
    """

    def __init__(self, js):
        "js is a string containing valid Javascript code."
        self.js = js


class CodeMirrorJSONEncoder(json.JSONEncoder):
    "A custom JSON encoder that knows how to handle CodeMirrorJavascript() objects."

    stash_prefix = "js_stash::"

    def __init__(self, *args, **kwargs):
        super(CodeMirrorJSONEncoder, self).__init__(*args, **kwargs)
        self.stash = {}

    def default(self, obj):
        def encode_if_necessary(x):
            try:
                x.encode
            except AttributeError:
                return x
            else:
                return x.encode("utf-8")

        if isinstance(obj, CodeMirrorJavascript):
            # If a Javascript object is encountered, replace it with a placeholder.
            stash_id = (
                self.stash_prefix
                + hashlib.md5(encode_if_necessary(obj.js)).hexdigest())
            self.stash[stash_id] = obj.js
            return stash_id
        return super(CodeMirrorJSONEncoder, self).default(obj)

    def encode(self, obj):
        self.stash = {}
        encoded = super(CodeMirrorJSONEncoder, self).encode(obj)
        # Search for any placeholders and replace them with their original values.
        for key, val in self.stash.items():
            encoded = encoded.replace('"' + key + '"', val)
        self.stash = {}
        return encoded
