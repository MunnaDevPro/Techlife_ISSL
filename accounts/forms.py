from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUserModel

class CustomUserSignupForm(UserCreationForm):
    mobile = forms.CharField(required=False, max_length=15)

    class Meta:
        model = CustomUserModel
        fields = ["first_name", "last_name", "email", "mobile", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        # Ensure username field isn't used (if you set username = None)
        try:
            user.username = None
        except Exception:
            pass
        # assign mobile if present
        user.mobile = self.cleaned_data.get("mobile") or ""
        if commit:
            user.save()
        return user