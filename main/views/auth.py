# ~*~ encoding: utf-8 ~*~

from django.conf import settings
from django.contrib.auth import login as djlogin, logout as djlogout, authenticate
from django.contrib import messages
from django import http
from django.shortcuts import render

from main.forms.auth import SigninForm, SignupForm
from main.models import User
from utils.decorators import reverse_lazy

import logging
logger = logging.getLogger(__name__)


def signin(request):
    if request.method == "POST":
        form = SigninForm(request.POST)
        if form.is_valid():
            cdata = form.cleaned_data
            args = {"password": cdata.get("password")}
            if "@" in cdata.get("username"):
                args.update({"email": cdata.get("username")})
            else:
                args.update({"username": cdata.get("username")})
            user = authenticate(**args)
            if user:
                if user.is_verified:
                    djlogin(request, user)
                    return http.HttpResponseRedirect("/")
                else:
                    return http.HttpResponseRedirect(reverse_lazy("verify"))
        messages.error(request, "Authentication failed, please check your credentials")
    else:
        form = SigninForm()
    return render(request, "main/auth/signin.jinja")


def signout(request):
    djlogout(request)
    return http.HttpResponseRedirect("/")


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            cdata = form.cleaned_data
            cdata.update({"subscribed_to_newsletter": bool(request.POST.get("newsletter"))})
            user = User.objects.create(username=cdata.get("email"),
                                       first_name=cdata.get("first_name"),
                                       last_name=cdata.get("last_name"),
                                       email=cdata.get("email"),
                                       is_active=True
                                       )
            user.set_password(cdata.get("password"))
            user.save()

            if not settings.VERIFICATION_REQUIRED:
                """ email adresi doğrulaması gerekmiyorsa hemen login ediyoruz """
                user = authenticate(email=cdata.get("email"), password=cdata.get("password"))
                djlogin(request, user)
                return http.HttpResponseRedirect("/")
            else:
                return http.HttpResponseRedirect(reverse_lazy("verify"))

        messages.error(request, "Please fix the following errors")
    else:
        form = SignupForm()
    return render(request, "main/auth/register.jinja")


def verify(request):
    code = request.GET("code")
    email = request.GET("email")
    user = authenticate(email=email, code=code)
    if user:
        djlogin(request, user)
        return http.HttpResponseRedirect("/")
    messages.error(request, "Unknown email address or wrong verification code, please check your input")
    return render(request, "main/auth/verify.jinja")
