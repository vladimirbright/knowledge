# -*- coding: utf8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from knowledge.cards.models import Cards, CardsPostForm


# 
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
            return render_to_response('index.html', { "postForm": form, "user": request.user, "title": u"Здесь будет база знаний."})
    else:
        form = CardsPostForm()
        cards = Cards.objects.all()
        return render_to_response('index.html', { "postForm": form, "cards": cards, "user": request.user, "title": u"Здесь будет база знаний."})


@login_required
def new_card(request):
    return render_to_response('index.html', { "user": request.user, "title": u"Здесь будет база знаний."})
