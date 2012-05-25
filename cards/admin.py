# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.comments.moderation import CommentModerator, moderator


from cards.models import Cards, Tag, Category


class CardsAdmin(admin.ModelAdmin):
    list_display  = ('topic', 'owner', 'tag', 'added')
    list_editable = ('tag',)
    ordering      = ('-added', )
    search_fields = ['topic',]
    date_hierarchy = 'added'
    list_filter = ('owner',)
admin.site.register(Cards, CardsAdmin)


class CardsModerator(CommentModerator):
    email_notification = True
moderator.register(Cards, CardsModerator)

class TagInline(admin.TabularInline):
    model = Tag

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'has_cards', 'sort')
    list_editable = ('sort',)
    inlines = [ TagInline ]
admin.site.register(Category, CategoryAdmin)


class TagAdmin(admin.ModelAdmin):
    pass
admin.site.register(Tag, TagAdmin)
