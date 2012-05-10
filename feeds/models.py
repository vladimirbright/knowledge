# -*- coding: utf-8 -*-

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse


from cards.models import Cards


class LastCardsFeed(Feed):
    ''' Main page RSS'''
    title = u'Последние заметки с knbase.org'
    link = '/last/'
    description = u'Последние заметки и решения с knbase.org'

    def items(self):
        return Cards.objects.order_by('-pk')[:5]

    def item_link(self, obj):
        return reverse('details', args=[obj.pk])

