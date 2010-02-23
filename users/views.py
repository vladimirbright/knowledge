# -*- coding: utf8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from knowledge.users.models import UserRegisterForm


def details(request, username):
    '''Инфа о пользователе'''
    user = get_object_or_404(User, username=username)
    return render_to_response('user.html', { 'user': user }, context_instance=RequestContext(request))


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

