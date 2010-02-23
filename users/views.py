# -*- coding: utf8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from knowledge.users.models import UserRegisterForm


def details(request, username):
    '''Инфа о пользователе'''
    return HttpResponse('ololo')


@login_required
def edit(request):
    '''Редактирование своей инфы'''
    return HttpResponse('lelele')


def register(request):
    '''Страница регистрации'''
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
    else:
        form = UserRegisterForm()
    return render_to_response('registration/register.html', {
        "title": u"Регистрация",
        "form": form,
    })

