from django import forms

class MultiLineCharField(forms.CharField):
    widget = forms.Textarea