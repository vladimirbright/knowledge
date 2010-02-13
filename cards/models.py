# -*- coding: utf8 -*-

from django.db import models
from datetime  import datetime
from django.contrib.auth.models import User
from django.contrib import admin
from django import forms

# Create your models here.

# Модель записи
class Cards(models.Model):
    topic     = models.CharField(max_length=140,verbose_name=u"Название")
    cardtext  = models.TextField(verbose_name=u"Заметка")
    formatted = models.TextField(blank=True)
    owner     = models.ForeignKey(User,verbose_name=u'Добавил')
    added     = models.DateTimeField(default=datetime.now(), verbose_name=u'Добавлена')

    def __unicode__(self):
        return u"<Заметка: %s>" %self.topic[:20]

    class Meta:
        verbose_name = u'Заметку'
        verbose_name_plural = u'Заметка'

class CardFavorites(models.Model):
    card  = models.ForeignKey(Cards,verbose_name=u'Заметка')
    owner = models.ForeignKey(User,verbose_name=u'Добавил')
    added = models.DateTimeField(default=datetime.now(), verbose_name=u'Добавлена в избранное')

    def __unicode__(self):
        return u"<Избранная заметка: %s, пользователя: %s>" %(self.card.topic[:20], self.owner.username)

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

    def save(self, owner):
        ''' Save new Card '''
        card           = Cards()
        card.topic     = self.cleaned_data["topic"]
        card.cardtext  = self.cleaned_data["cardtext"]
        card.owner     = owner
        card.formatted = format_code(self.cleaned_data["cardtext"])
        card.save()
        return True

def format_code(text):
    '''Function to find [code] tags and replace with highlited code'''
    if len(text) < 10:
        return text

    import re
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import HtmlFormatter
    from pygments.styles import get_style_by_name

    # Пробуем найти запастенный код.
    code_pattern = re.compile(r'\[code=([^\]]+)\]', re.M+re.I)

    open_tag_pat = '[code=%s]'
    close_tag    = '[/code]'

    code = code_pattern.findall(text)

    if len(code) > 0:

        for prog_lang in code:
            try:
                # Ищем начало кода
                open_tag = open_tag_pat %prog_lang
                start    = text.index(open_tag)
                start   += len(open_tag)
                # Ищем окончание кода.
                end       = text[start:].index(close_tag)
                code_text = text[start:start+end]

                lexer          = get_lexer_by_name(prog_lang, stripall=True)
                formatter      = HtmlFormatter(linenos=True, noclasses=True, style='perldoc')
                code_formatted = highlight(code_text, lexer, formatter)

                text = text.replace( open_tag + code_text + close_tag, u"<h5>Код: %s</h5>%s" %(lexer.name, code_formatted))
            except:
                pass

    return text

