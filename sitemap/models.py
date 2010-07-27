# -*- coding: utf8 -*-

from django.contrib.sitemaps import Sitemap

from cards.models import Cards


class CardsSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Cards.objects.all()

    def lastmod(self, obj):
        return obj.added

