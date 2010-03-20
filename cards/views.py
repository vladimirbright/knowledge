# -*- coding: utf8 -*-

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.db import connection
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from knowledge.cards.models import Cards, CardsPostForm, CardFavorites
from knowledge.settings import PER_PAGE, PAGE_GET


# Главная страница.
def index(request, best=False):
    '''Главная страница'''
    order = '-pk'
    title = None
    currentplace = 'Последние записи'
    if best is True:
        order = '-rating'
        title = ':: Самые популярные'
        currentplace = 'Популярные записи'

    cards_list = Cards.objects.select_related().all().order_by(order)
    paginator = Paginator(cards_list, PER_PAGE)

    try:
        page = int(request.GET.get(PAGE_GET, '1'))
    except ValueError:
        page = 1

    try:
        cards = paginator.page(page)
    except (EmptyPage, InvalidPage):
        cards = paginator.page(paginator.num_pages)

    user  = request.user
    favorites = False

    if user.is_authenticated() is True:
        favorites = user.cardfavorites_set.all()
        for card in cards.object_list:
            card.in_favorite = False
            for f in favorites:
                if f.card_id == card.pk:
                    card.in_favorite = True
                    break

    if request.method == 'POST' and user.is_authenticated():
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
                                        "title" : title,
                                        "currentplace": currentplace,
                                        #"queries" : connection.queries
                                        }, context_instance=RequestContext(request))


def search(request):
    '''Страница поиска'''
    cards = []
    user  = request.user

    try:
        search_term  = request.GET.get('q', '')
    except ValueError:
        search_term = ''

    search_term = search_term.strip()

    if search_term != '':
        cards = Cards.search.query(search_term)[0:PER_PAGE]

    return render_to_response('search.html', {
                                'search_term' : search_term,
                                'cards': cards,
                                'user': user,
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
    favorites = user.cardfavorites_set.select_related().all().order_by('-added')
    cards_list = []

    for f in favorites:
        card = f.card
        card.in_favorite = True
        cards_list.append(card)

    paginator = Paginator(cards_list, PER_PAGE)

    try:
        page = int(request.GET.get(PAGE_GET, '1'))
    except ValueError:
        page = 1

    try:
        cards = paginator.page(page)
    except (EmptyPage, InvalidPage):
        cards = paginator.page(paginator.num_pages)

    form = CardsPostForm()
    return render_to_response('index.html', {
                                        "postForm": form,
                                        "cards": cards,
                                        "user": user,
                                        "favorites": favorites,
                                        "currentplace": u"Избранные заметки",
                                        "title": u":: Избранные заметки",
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

        card.rating += 1
        card.save()
    except:
        pass
    return HttpResponseRedirect('/')


@login_required
def fav_del(request, card_id):
    try:
        favorite = CardFavorites.objects.filter(card=card_id,owner=request.user)
        favorite.delete()
        card = Cards.objects.get(pk=card_id)
        if card.rating > 0:
            card.rating -= 1
            card.save()
    except:
        pass
    return HttpResponseRedirect(reverse('knowledge.cards.views.favorites'))


# Страница по рейтингу.
def rating(request):
    return index(request, best=True)

#
