# -*- coding: utf8 -*-

from django.db import models
from datetime  import datetime
from django.contrib.auth.models import User

from django import forms

# Create your models here.

# Модель записи
class Cards(models.Model):
    topic    = models.CharField(max_length=140,verbose_name=u"Название")
    cardtext = models.TextField(verbose_name=u"Заметка")
    owner    = models.ForeignKey(User)
    added    = models.DateTimeField(default=datetime.now(), verbose_name=u'Добавлена')

    def __unicode__(self):
        return u"<Заметка: %s>" %self.topic[:20]

class CardsPostForm(forms.Form):
    topic    = forms.CharField(max_length=140,label=u"Название")
    cardtext = forms.CharField(label=u"Заметка",widget=forms.Textarea)
