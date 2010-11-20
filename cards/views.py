# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.conf import settings

from cards.models import Cards, CardFavorites, CardsModelPostForm, CardsImage
from cards.models import format_code


PER_PAGE  = getattr(settings, 'PER_PAGE', 5)
PAGE_GET = getattr(settings, 'PAGE_GET', 'page')


# Главная страница.
def index(request, best=False):
    '''Главная страница'''
    order = '-pk'
    title = None
    currentplace = u'Последние записи'
    if best is True:
        order = '-rating'
        title = u':: Самые популярные'
        currentplace = u'Популярные записи'

    cards = Cards.objects.select_related('owner').order_by(order)

    user  = request.user
    favorites = False
    form = None

    # Проверку вынесу в тэг
    #if user.is_authenticated() is True:
        #favorites = user.cardfavorites_set.all()
        #for card in cards.object_list:
            #card.in_favorite = False
            #for f in favorites:
                #if f.card_id == card.pk:
                    #card.in_favorite = True
                    #break

    if user.is_authenticated():
        form = CardsModelPostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            newcard = form.save(commit=False)
            newcard.owner = user
            newcard.save()
            return HttpResponseRedirect(reverse('cards.views.details', args=[newcard.pk]))
    return render_to_response('index.html', {
                                        "postForm": form,
                                        "cards": cards,
                                        "user": user,
                                        "favorites": favorites,
                                        "title" : title,
                                        "currentplace": currentplace,
                                        }, context_instance=RequestContext(request))


# Страница по рейтингу.
def rating(request):
    return index(request, best=True)


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
    return render_to_response('search.html', locals(), context_instance=RequestContext(request))



# Страница подробностей.
def details(request, card_id):
    user = request.user
    card = get_object_or_404(Cards, pk=card_id)
    card.in_favorite = False
    if user.is_authenticated() is True:
        fav = CardFavorites.objects.filter(card=card.pk,owner=user.pk)
        if len(fav) > 0:
            card.in_favorite = True
    return render_to_response('details.html', locals(), context_instance=RequestContext(request))


@login_required
def edit(request, card_id):
    card = get_object_or_404(Cards, pk=card_id)
    user = request.user
    if not user.has_perm('cards.change_cards') and card.owner.pk != user.pk:
        return HttpResponseRedirect('/')
    form = CardsModelPostForm(request.POST or None, request.FILES or None,
                                                                 instance=card)
    # preview
    if form.is_valid():
        card = form.save(commit=False)
        if 'preview' in request.POST:
            card.formatted = format_code(card.cardtext)
        else:
            card.save()
            return HttpResponseRedirect(reverse('cards.views.details', args=[card.pk]))
    return render_to_response('edit.html', locals(), context_instance=RequestContext(request))


# Страница избранного.
@login_required
def favorites(request):
    '''Страница с избранным'''
    cards = request.user.cardfavorites_set.select_related('owner').order_by('-pk')
    form = CardsModelPostForm()
    return render_to_response('cards/favorites.html', {
                                        "postForm": form,
                                        "cards": cards,
                                        "currentplace": u"Избранные заметки",
                                        "title": u":: Избранные заметки",
                                        }, context_instance=RequestContext(request))


def action_with_favorites(request, card_id, delete=False):
    try:
        card = Cards.objects.get(pk=card_id)
        if delete is False:
            favorite = CardFavorites()
            favorite.owner = request.user
            favorite.card  = card
            favorite.save()
            card.rating += 1
            card.save()
        else:
            favorite = CardFavorites.objects.filter(card=card_id,owner=request.user)
            favorite.delete()
            if card.rating > 0:
                card.rating -= 1
                card.save()
    except ObjectDoesNotExist:
        pass
    try:
        from_details = request.GET['from_details']
    except:
        return HttpResponseRedirect(reverse('cards.views.favorites'))
    else:
        return HttpResponseRedirect(reverse('cards.views.details', args=[card.pk]))


@login_required
def fav_add(request, card_id):
    return action_with_favorites(request, card_id, False)


@login_required
def fav_del(request, card_id):
    return action_with_favorites(request, card_id, True)



#
