# -*- coding: utf-8 -*-

from cards.models import Category


def get_favorites(request):
    if request.user.is_authenticated() is False:
        return {}
    favorites = request.user.cardfavorites_set\
                                        .select_related('card', 'owner')\
                                        .order_by('-pk')
    cards = [ i.card.pk for i in favorites ]
    return { "cards_favorites": cards }


def get_categories(request):
    return { "site_categories": Category.objects.filter(has_cards=True) }

