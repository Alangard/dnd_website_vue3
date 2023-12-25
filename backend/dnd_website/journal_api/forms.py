from django import forms
from django.contrib.auth import forms as auth_forms
from .models import Account

class MultiLineCharField(forms.CharField):
    widget = forms.Textarea

class UserCreationForm(auth_forms.UserCreationForm):
    class Meta(auth_forms.UserCreationForm.Meta):
        model = Account
        fields = ("username", "email")