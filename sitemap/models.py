# -*- coding: utf-8 -*-

from django.contrib.sitemaps import Sitemap

from cards.models import Cards, Category, Tag


class CardsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Cards.objects.all()

    def lastmod(self, obj):
        return obj.added


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Category.objects.filter(has_cards=True)

    def lastmod(self, obj):
        try:
            return Cards.objects.filter(tag__category=obj)[:1][0].added
        except IndexError:
            return None


class TagSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Tag.objects.filter(has_cards=True)

    def lastmod(self, obj):
        try:
            return Cards.objects.filter(tag=obj)[:1][0].added
        except IndexError:
            return None

