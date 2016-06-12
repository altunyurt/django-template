# ~*~ encoding: utf-8 ~*~

from django import forms
from main.models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ["ip_address", "status"]

        widgets = {
            "message": forms.Textarea(attrs={"rows": 3})
        }
