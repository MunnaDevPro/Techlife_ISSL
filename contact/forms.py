from django import forms
from .models import contact_or_support

class ContactOrSupportForm(forms.ModelForm):
    class Meta:
        model = contact_or_support
        fields = ['name', 'email', 'phone', 'message']
