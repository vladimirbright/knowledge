# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render


from cards.models import Cards, CardFavorites, CardsModelPostForm, format_code


PER_PAGE = getattr(settings, 'PER_PAGE', 5)
PAGE_GET = getattr(settings, 'PAGE_GET', 'page')


# Главная страница.
def index(request, best=False):
    '''Главная страница'''
    order = '-pk'
    title = None
    if best is True:
        order = '-rating'
        title = u':: Самые популярные'

    cards = Cards.objects.select_related('owner').order_by(order)

    user  = request.user
    form = None

    if user.is_authenticated():
        form = CardsModelPostForm(
                    request.POST or None,
                    request.FILES or None
                )
        if form.is_valid():
            with transaction.commit_on_success():
                newcard = form.save(commit=True, owner=user)
            return HttpResponseRedirect(newcard.get_absolute_url())
    nav = dict(usefull=True) if best else dict(last=True)
    return render(request, 'index.html', {
                                        "postForm": form,
                                        "cards": cards,
                                        "user": user,
                                        "title" : title,
                                        "nav": nav,
                                        })


# Страница по рейтингу.
def rating(request):
    return index(request, best=True)


# Страница подробностей.
def details(request, card_id):
    user = request.user
    card = get_object_or_404(Cards, pk=card_id)
    card.in_favorite = False
    if user.is_authenticated() is True:
        card.in_favorite = CardFavorites.objects\
                                        .filter(card=card, owner=user)\
                                        .exists()
    return render(request, 'cards/details.html', dict(card=card))


@login_required
def edit(request, card_id):
    card = get_object_or_404(Cards, pk=card_id)
    user = request.user
    if not user.has_perm('cards.change_cards') and \
       card.owner.pk != user.pk:
        return HttpResponseRedirect('/')
    form = CardsModelPostForm(
                request.POST or None,
                request.FILES or None,
                instance=card
            )
    # preview
    if form.is_valid():
        card = form.save(commit=False)
        if 'preview' in request.POST:
            card.formatted = format_code(card.cardtext)
        else:
            card.save()
            return HttpResponseRedirect(card.get_absolute_url())
    return render(request, 'edit.html', locals())


# Страница избранного.
@login_required
def favorites(request):
    '''Страница с избранным'''
    favorites = list(request.user.cardfavorites_set\
                        .order_by('-pk'))
    cards = []
    if favorites:
        cards = Cards.objects.filter(pk__in=[ i.card_id for i in favorites])
    form = CardsModelPostForm()
    return render(
                request,
                'index.html',
                dict(
                    postForm=form,
                    cards=cards,
                    title=u":: Избранные заметки",
                    nav=dict(favorites=True)
                )
            )


def action_with_favorites(request, card_id, delete=False):
    card = get_object_or_404(Cards, pk=card_id)
    if delete is False:
        favorite = CardFavorites(owner=request.user, card=card)
        favorite.save()
        card.rating += 1
        card.save()
    else:
        favorite = get_object_or_404(CardFavorites,
                                     card=card,
                                     owner=request.user)
        favorite.delete()
        if card.rating > 0:
            card.rating -= 1
            card.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER",
                                             reverse('cards.views.favorites')))


@login_required
def fav_add(request, card_id):
    return action_with_favorites(request, card_id, False)


@login_required
def fav_del(request, card_id):
    return action_with_favorites(request, card_id, True)



#
