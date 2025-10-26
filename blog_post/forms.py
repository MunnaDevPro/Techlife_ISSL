from django import forms
from .models import Category


class IconForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "font_awesome_icon" , "description"]
