# -*- coding: utf8 -*-

from django.db import models
from datetime  import datetime
from django.contrib.auth.models import User
from django.contrib import admin
from django import forms

# Create your models here.

# Модель записи
class Cards(models.Model):
    topic    = models.CharField(max_length=140,verbose_name=u"Название")
    cardtext = models.TextField(verbose_name=u"Заметка")
    owner    = models.ForeignKey(User,verbose_name=u'Добавил')
    added    = models.DateTimeField(default=datetime.now(), verbose_name=u'Добавлена')

    def __unicode__(self):
        return u"<Заметка: %s>" %self.topic[:20]

    class Meta:
        verbose_name = u'Заметку'
        verbose_name_plural = u'Заметка'

class CardsAdmin(admin.ModelAdmin):
    #fields        = ('topic', 'owner', 'added')
    list_display  = ('topic', 'owner', 'added')
    ordering      = ('-added', )
    search_fields = ['topic',]
    date_hierarchy = 'added'
    fieldsets = (
            (None, {
                'fields': ('topic', 'cardtext', 'owner', 'added')
            }),
        )


admin.site.register(Cards, CardsAdmin)


class CardsPostForm(forms.Form):
    topic    = forms.CharField(max_length=140,label=u"Название")
    cardtext = forms.CharField(label=u"Заметка",widget=forms.Textarea)

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
