# -*- coding: utf8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.http import HttpResponse
from knowledge.users.models import UserRegisterForm



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
    else:
        form = UserRegisterForm()
    return render_to_response('registration/register.html', {
        "title": u"Регистрация в базе!",
        "form": form,
    })

