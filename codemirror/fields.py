from django.db import models
from django import forms

from codemirror.widgets import CodeMirrorTextarea


class CodeMirrorField(models.TextField):
    def formfield(self, **kwargs):
        defaults = {
            'form_class': CodeMirrorFormField,
        }
        defaults.update(kwargs)
        return super(CodeMirrorField, self).formfield(**defaults)


class CodeMirrorFormField(forms.fields.Field):
    def __init__(self, *args, **kwargs):
        kwargs.update({'widget': CodeMirrorTextarea})
        super(CodeMirrorFormField, self).__init__(*args, **kwargs)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^codemirror\.fields\.CodeMirrorField"])
except:
    pass

