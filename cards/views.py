# -*- coding: utf8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from knowledge.cards.models import Cards, CardsPostForm


# Главная страница.
# Тут пагинацию прикрутить.
def index(request):
    if request.method == 'POST' and request.user.is_authenticated:
        form = CardsPostForm(request.POST)
        if form.is_valid():
            card = Cards()
            card.topic    = form.cleaned_data["topic"]
            card.cardtext = form.cleaned_data["cardtext"]
            card.owner    = request.user
            card.save()
            return HttpResponseRedirect('/')
        else:
            cards = Cards.objects.all().order_by('-pk')
            return render_to_response('index.html', {
                                                        "cards": cards,
                                                        "postForm": form,
                                                        "user": request.user,
                                                        "title": u"Здесь будет база знаний."
                                                        })
    else:
        form = CardsPostForm()
        cards = Cards.objects.all().order_by('-pk')
        return render_to_response('index.html', { "postForm": form, "cards": cards, "user": request.user, "title": u"Здесь будет база знаний."})


# Страница подробностей.
def details(request, card_id):
    return HttpResponse(u'Нет пока никто, но будет описание с комментами для ' + str(card_id) + u' заметки.')

#
