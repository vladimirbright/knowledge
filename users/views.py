# -*- coding: utf-8 -*-

from django.conf  import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render

from users.models import UserRegisterForm, UserSettingsForm
from cards.models import Cards


PER_PAGE  = getattr(settings, 'PER_PAGE', 5)
PAGE_GET = getattr(settings, 'PAGE_GET', 'page')


def details(request, username):
    u'''Инфа о пользователе'''
    user = get_object_or_404(User, username=username)
    # Зашли ли мы с свой профиль?
    user.self_request = False
    if user == request.user:
        user.self_request = True
    cards = Cards.objects.filter(owner=user).order_by('-pk')
    c = dict(
        viewed_user=user,
        user=request.user ,
        cards=cards,
    )
    return render(request, 'users/user.html', c)


@login_required
def edit(request):
    '''Редактирование своей инфы'''
    defaults = {
                   'username': request.user.username,
                   'email': request.user.email
               }
    if request.method == 'POST':
        form = UserSettingsForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            return HttpResponseRedirect("/settings/")
    else:
        form = UserSettingsForm(initial=defaults)
    return render(request, 'users/usersettings.html', {
                                            'user': request.user ,
                                            'form': form,
                                            'nav': dict(settings=True),
                                            })


