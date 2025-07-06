# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
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
    # Simple response for now due to template URL issues
    from django.http import HttpResponse
    cards = Cards.objects.select_related(
                              'owner',
                              'tag',
                              'tag__category'
                          ).order_by('-pk')[:10]  # Limit for display
    
    html = """
    <h1>Knowledge Base</h1>
    <p><a href="/admin/">Admin Panel</a> | <a href="/admin/cards/cards/add/">Add New Card</a></p>
    <h2>Recent Cards ({} total)</h2>
    """.format(Cards.objects.count())
    
    for card in cards:
        html += f"""
        <div style="border: 1px solid #ccc; margin: 10px; padding: 10px;">
            <h3><a href="/admin/cards/cards/{card.pk}/change/">{card.topic}</a></h3>
            <p>By: {card.owner.username} on {card.added.strftime('%Y-%m-%d %H:%M')}</p>
            <div>{card.formatted or card.cardtext}</div>
        </div>
        """
    
    if not cards:
        html += "<p>No cards yet. <a href='/admin/cards/cards/add/'>Create your first card!</a></p>"
    
    return HttpResponse(html)

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
