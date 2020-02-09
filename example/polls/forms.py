from django import forms
from codemirror import CodeMirrorTextarea


widget = CodeMirrorTextarea(
    mode="python", theme="cobalt", config={"fixedGutter": True,}
)


class SampleForm(forms.Form):
    body = forms.CharField(label="Body", widget=widget)

