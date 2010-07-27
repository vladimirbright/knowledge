# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.comments.moderation import CommentModerator, moderator

from cards.models import *


class CardsAdmin(admin.ModelAdmin):
    #fields        = ('topic', 'owner', 'added')
    list_display  = ('topic', 'owner', 'added')
    ordering      = ('-added', )
    search_fields = ['topic',]
    date_hierarchy = 'added'
    list_filter = ('owner',)


admin.site.register(Cards, CardsAdmin)


class CardsModerator(CommentModerator):
    email_notification = True

moderator.register(Cards, CardsModerator)
