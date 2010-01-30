# -*- coding: utf8 -*-

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django.contrib.auth.decorators import login_required

from knowledge.cards.models import Cards, CardsPostForm


# Главная страница.
# Тут пагинацию прикрутить.
def index(request):
    '''Главная страница'''

    sort = '-pk'

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
            cards = Cards.objects.all().order_by(sort)
            return render_to_response('index.html', {
                                                        "cards": cards,
                                                        "postForm": form,
                                                        "user": request.user,
                                                        "title": u"Здесь будет база знаний."
                                                        }, context_instance=RequestContext(request))
    else:
        form = CardsPostForm()
        cards = Cards.objects.all().order_by(sort)
        return render_to_response('index.html', {
                                            "postForm": form,
                                            "cards": cards,
                                            "user": request.user
                                            }, context_instance=RequestContext(request))


# Страница подробностей.
def details(request, card_id):
        card = get_object_or_404(Cards, pk=card_id)
        return render_to_response('details.html', { "card": card, "user": request.user }, context_instance=RequestContext(request))

# Страница избранного.
def favorites(request):
        card = get_object_or_404(Cards, pk=card_id)
        return render_to_response('details.html', { "card": card, "user": request.user }, context_instance=RequestContext(request))

# Страница по рейтингу.
def rating(request):
        card = get_object_or_404(Cards, pk=card_id)
        return render_to_response('details.html', { "card": card, "user": request.user }, context_instance=RequestContext(request))

#
