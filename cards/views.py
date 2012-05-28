# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView


from cards.models import (
    CardFavorites,
    Cards,
    CardsModelPostForm,
    Category,
    format_code,
    Tag,
)


PER_PAGE = getattr(settings, 'PER_PAGE', 5)
PAGE_GET = getattr(settings, 'PAGE_GET', 'page')


class CardDetailView(DetailView):
    queryset = Cards.objects.all()
    context_object_name='card'

    def get_context_data(self, **kwargs):
        context = super(CardDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        card = context['card']
        if card.tag_id:
            context['current_category'] = card.tag.category
            context['current_tag'] = card.tag
            context['nav'] = dict(
                            current_category_id=card.tag.category_id,
                            current_tag_id=card.tag_id
                        )
        return context


# Главная страница.
def index(request, category_slug=None, tag_slug=None):
    '''Главная страница'''
    cards = Cards.objects.select_related(
                              'owner',
                              'tag',
                              'tag__category'
                          ).order_by('-pk')
    current_category = None
    current_tag = None
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        if not tag_slug:
            cards = cards.filter(tag__category=current_category)
        else:
            current_tag = get_object_or_404(Tag, slug=tag_slug)
            cards = cards.filter(tag=current_tag)

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
    nav = {}
    if not any((current_category, current_tag)):
        nav['last'] = True
    if current_category:
        nav['current_category_id'] = current_category.pk
    if current_tag:
        nav['current_tag_id'] = current_tag.pk
    return render(request, 'index.html', {
                                    "postForm": form,
                                    "cards": cards,
                                    "user": user,
                                    "nav": nav,
                                    "current_tag": current_tag,
                                    "current_category": current_category,
                                })

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
