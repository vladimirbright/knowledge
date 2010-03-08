# -*- coding: utf8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.db import connection
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from knowledge.users.models import UserRegisterForm
from knowledge.cards.models import Cards
from knowledge.settings import PER_PAGE, PAGE_GET


def details(request, username):
    '''Инфа о пользователе'''
    user = get_object_or_404(User, username=username)
    # Зашли ли мы с свой профиль?
    user.self_request = False
    if user == request.user:
        user.self_request = True

    try:
        page = int(request.GET.get(PAGE_GET, '1'))
    except ValueError:
        page = 1

    cards_list = Cards.objects.filter(owner=user).order_by('-pk')
    paginator = Paginator(cards_list, PER_PAGE)

    try:
        cards = paginator.page(page)
    except (EmptyPage, InvalidPage):
        cards = paginator.page(paginator.num_pages)

    return render_to_response('user.html', {
                                            'viewed_user': user,
                                            'user': request.user ,
                                            'cards': cards,
                                            #'queries' : connection.queries
                                            }, context_instance=RequestContext(request))


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

