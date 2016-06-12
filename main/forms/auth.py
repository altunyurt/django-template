# ~*~ encoding: utf-8 ~*~

from django import forms
from main.models import User


class SigninForm(forms.Form):
    username = forms.CharField(max_length=100, required=True,
                               label="Username or E-mail",
                               widget=forms.TextInput(attrs={"ng-model": "username"}))
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(), label="Password")


class SignupForm(forms.Form):
    email = forms.EmailField(required=True, label="E-mail Address")
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput())

    def clean_confirm_password(self):
        p1 = self.cleaned_data.get("password")
        p2 = self.cleaned_data.get("confirm_password")

        if p1 == p2:
            return p2
        raise forms.ValidationError("Passwords don't match")

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data.get("email")).exists():
            raise forms.ValidationError("This email address is already registered")
        return self.cleaned_data.get("email")


class VerificationForm(forms.Form):
    code = forms.CharField(max_length=40, required=True)
