# -*- coding: utf8 -*-

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.db import connection

from django.contrib.auth.decorators import login_required

from knowledge.cards.models import Cards, CardsPostForm, CardFavorites


# Главная страница.
# Тут пагинацию прикрутить.
def index(request):
    '''Главная страница'''
    cards = Cards.objects.all().order_by('-pk')
    user  = request.user
    favorites = False

    if user.is_authenticated() is True:
        favorites = user.cardfavorites_set.all()
        for card in cards:
            card.in_favorite = False
            for f in favorites:
                if f.card == card:
                    card.in_favorite = True
                    break

    if request.method == 'POST' and user.is_authenticated:
        form = CardsPostForm(request.POST)
        if form.is_valid():
            form.save(user)
            return HttpResponseRedirect('/')
    else:
        form = CardsPostForm()

    return render_to_response('index.html', {
                                        "postForm": form,
                                        "cards": cards,
                                        "user": user,
                                        "favorites": favorites,
                                        #"queries" : connection.queries
                                        }, context_instance=RequestContext(request))


# Страница подробностей.
def details(request, card_id):
    card = get_object_or_404(Cards, pk=card_id)
    return render_to_response('details.html', { "card": card, "user": request.user }, context_instance=RequestContext(request))

# Страница избранного.
@login_required
def favorites(request):
    '''Страница с избранным'''

    user  = request.user
    favorites = user.cardfavorites_set.select_related().all().order_by('-pk')
    cards = []

    for f in favorites:
        card = f.card
        card.in_favorite = True
        cards.append(card)

    form = CardsPostForm()

    return render_to_response('index.html', {
                                        "postForm": form,
                                        "cards": cards,
                                        "user": user,
                                        "favorites": favorites,
                                        #"queries" : connection.queries
                                        }, context_instance=RequestContext(request))

@login_required
def fav_add(request, card_id):
    try:
        card = Cards.objects.get(pk=card_id)
        favorite = CardFavorites()
        favorite.owner = request.user
        favorite.card  = card
        favorite.save()
    except:
        pass

    return HttpResponseRedirect('/')

@login_required
def fav_del(request, card_id):
    try:
        favorite = CardFavorites.objects.filter(card=card_id,owner=request.user)
        favorite.delete()
    except:
        pass

    return HttpResponseRedirect('/')

# Страница по рейтингу.
def rating(request):
    card = get_object_or_404(Cards, pk=card_id)
    return render_to_response('details.html', { "card": card, "user": request.user }, context_instance=RequestContext(request))

#
