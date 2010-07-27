# -*- coding: utf8 -*-

from django.db import models
from datetime  import datetime
from django.contrib.auth.models import User
from django.contrib import admin
from django import forms
from django.contrib.comments.signals import comment_was_posted, comment_was_flagged
from django.contrib.comments.moderation import CommentModerator, moderator

from djangosphinx.models import SphinxSearch


class Cards(models.Model):
    ''' Main Card model'''
    topic     = models.CharField(max_length=140,verbose_name=u"Название")
    # Исходный текст заметки
    cardtext  = models.TextField(verbose_name=u"Заметка")
    # Посвеченный текст заметки
    formatted = models.TextField(blank=True)
    owner     = models.ForeignKey(User,verbose_name=u'Добавил')
    added     = models.DateTimeField(default=datetime.now(), verbose_name=u'Добавлена')
    comments  = models.IntegerField(default=0,verbose_name=u'Кол-во комментариев')
    rating    = models.IntegerField(default=0,verbose_name=u'Рейтинг заметки')

    objects = models.Manager()
    search  = SphinxSearch(index="cards")

    def __unicode__(self):
        return u"<Заметка: %s>" %self.topic[:60]

    @models.permalink
    def get_absolute_url(self):
        return ('cards.views.details', [ self.pk, ])

    class Meta:
        verbose_name = u'Заметку'
        verbose_name_plural = u'Заметка'


class CardsAdmin(admin.ModelAdmin):
    #fields        = ('topic', 'owner', 'added')
    list_display  = ('topic', 'owner', 'added')
    ordering      = ('-added', )
    search_fields = ['topic',]
    date_hierarchy = 'added'
    list_filter = ('owner',)
    fieldsets = (
            (None, {
                'fields': ('topic', 'cardtext', 'owner', 'added')
            }),
        )


admin.site.register(Cards, CardsAdmin)


class CardsModerator(CommentModerator):
    email_notification = True


moderator.register(Cards, CardsModerator)


class CardFavorites(models.Model):
    '''user - favorite  topic relationship'''
    card  = models.ForeignKey(Cards,verbose_name=u'Заметка')
    owner = models.ForeignKey(User,verbose_name=u'Добавил')
    added = models.DateTimeField(default=datetime.now(), verbose_name=u'Добавлена в избранное')

    def __unicode__(self):
        return u"Избранная заметка: %s, пользователя: %s" %(self.card.topic[:20], self.owner.username)


class CardsImage(models.Model):
    '''Screenshots img & etc'''
    card = models.ForeignKey(Cards,verbose_name=u'Заметка')
    owner = models.ForeignKey(User,verbose_name=u'Заливший')
    image = models.ImageField(upload_to='media/i/')

    def __unicode__(self):
        return u"Изображение для: %s" %(self.card.topic[:20])

class CardsPostForm(forms.Form):
    '''Form to post new topic'''
    topic    = forms.CharField(max_length=140,label=u"Название")
    cardtext = forms.CharField(label=u"Заметка",widget=forms.Textarea)
    images   = forms.ImageField(label=u"Скрин")

    def clean_topic(self):
        text = self.cleaned_data['topic'].strip()
        if text == '':
            raise forms.ValidationError(u'Ваши мысли пусты!')
        return text

    def clean_cardtext(self):
        text = self.cleaned_data['cardtext'].strip()
        if text == '':
            raise forms.ValidationError(u'Ваши мысли пусты!')
        if len(text.split()) < 2:
            raise forms.ValidationError(u'Ваши мысли очень скудны! Оставьте хотя бы пару слов.')
        return text

    def save(self, owner):
        ''' Save new Card '''
        card           = Cards()
        card.topic     = self.cleaned_data["topic"]
        card.cardtext  = self.cleaned_data["cardtext"]
        card.owner     = owner
        card.formatted = format_code(self.cleaned_data["cardtext"])
        card.save()
        if not self.cleaned_data["images"] is None:
            image = CardsImage()
            image.card = card
            image.owner= owner
            image.image= self.cleaned_data["images"]
            image.save()
        return card


class CardsEditForm(CardsPostForm):
    def save(self, card, preview=False):
        card.topic     = self.cleaned_data["topic"]
        card.cardtext  = self.cleaned_data["cardtext"]
        card.formatted = format_code(self.cleaned_data["cardtext"])
        if not images is None:
            image = CardsImage()
            image.card = card
            image.owner= owner
            image.save()
        if preview is False:
            card.save()
        else:
            return card


def format_code(text):
    '''Function to find [code] tags and replace with highlited code'''
    import bbcode
    return bbcode.to_html(text)

