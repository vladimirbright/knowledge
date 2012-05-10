# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django import forms


class Cards(models.Model):
    topic = models.CharField(u"Название", max_length=140)
    # Исходный текст заметки
    cardtext = models.TextField(u"Заметка")
    # Подсвеченный текст заметки
    formatted = models.TextField(blank=True)
    owner = models.ForeignKey(User, verbose_name=u'Добавил', editable=False)
    added = models.DateTimeField(u'Добавлена', auto_now_add=True)
    comments = models.IntegerField(u'Комментариев', default=0, editable=False)
    rating = models.IntegerField(u'Рейтинг заметки', editable=False, default=0)

    def __unicode__(self):
        return u"<Заметка: %s>" %self.topic[:60]

    @models.permalink
    def get_absolute_url(self):
        return ('cards.views.details', [ self.pk, ])

    def save(self, *args, **kwargs):
        if 'owner' in kwargs:
            self.owner = kwargs.pop('owner')
        self.formatted = format_code(self.cardtext)
        return super(Cards, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u'Заметку'
        verbose_name_plural = u'Заметка'


class CardFavorites(models.Model):
    '''user - favorite  topic relationship'''
    card  = models.ForeignKey(Cards, verbose_name=u'Заметка')
    owner = models.ForeignKey(User, verbose_name=u'Добавил')
    added = models.DateTimeField(u'Добавлена в избранное', auto_now_add=True)

    def __unicode__(self):
        return u"Избранная заметка: %s, пользователя: %s" %(self.card.topic[:20], self.owner.username)


class CardsImage(models.Model):
    '''Screenshots img & etc'''
    card = models.ForeignKey(Cards, verbose_name=u'Заметка')
    owner = models.ForeignKey(User, verbose_name=u'Заливший')
    image = models.ImageField(u'Изображение', upload_to='uploads/images')
    added = models.DateTimeField(u'Добавленo', auto_now_add=True)

    def __unicode__(self):
        return u"Изображение для: %s" %(self.card.topic[:20])


class CardsModelPostForm(forms.ModelForm):

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
            raise forms.ValidationError(
                    u'Ваши мысли очень скудны! '\
                    u'Оставьте хотя бы пару слов.'
                )
        return text

    def save(self, *args, **kwargs):
        if 'owner' in kwargs:
            self.instance.owner = kwargs.pop('owner')
        return super(CardsModelPostForm, self).save(*args, **kwargs)

    class Meta:
        model = Cards
        fields = ( 'topic', 'cardtext' )


def format_code(text):
    '''Function to find [code] tags and replace with highlited code'''
    import bbcode
    return bbcode.to_html(text)

