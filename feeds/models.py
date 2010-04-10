# -*- coding: utf8 -*-

from django.db import models
from django.contrib.syndication.feeds import Feed
from knowledge.cards.models import Cards
from django.core.urlresolvers import reverse
# Create your models here.

class LastCards(Feed):
    ''' Main page RSS'''
    title = u'Последние заметки с knbase.org'
    link = '/last/'
    description = u'Последние заметки и решения с knbase.org'

    def items(self):
        return Cards.objects.order_by('-pk')[:5]

    def item_link(self, obj):
        return reverse('details', args=[obj.pk])

