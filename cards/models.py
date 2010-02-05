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
        import re


        card           = Cards()
        card.topic     = self.cleaned_data["topic"]
        card.cardtext  = self.cleaned_data["cardtext"]
        card.owner     = owner

        # Пробуем найти запастенный код.
        code_pattern = re.compile(r'\[code=([^\]]+)\]', re.M+re.I)

        open_tag_pat = '[code=%s]'
        close_tag    = '[/code]'

        code = code_pattern.findall(self.cleaned_data["cardtext"])

        if len(code) > 0:
            from pygments import highlight
            from pygments.lexers import get_lexer_by_name
            from pygments.formatters import HtmlFormatter
            from pygments.styles import get_style_by_name

            card.formatted = self.cleaned_data['cardtext']
            for prog_lang in code:
                # Ищем начало кода
                open_tag = open_tag_pat %prog_lang
                start    = card.formatted.index(open_tag)
                start   += len(open_tag)
                # Ищем окончание кода.
                try:
                    end      = card.formatted[start:].index(close_tag)
                    code_text= card.formatted[start:start+end]
                except:
                    continue

                lexer = get_lexer_by_name(prog_lang, stripall=True)
                formatter = HtmlFormatter(linenos=True, noclasses=True, style='colorful')
                code_formatted = highlight(code_text, lexer, formatter)

                card.formatted = card.formatted.replace('[code=%s]%s[/code]' %(prog_lang, code_text), u"<h5>Код: %s</h5>%s" %(prog_lang, code_formatted))

        else:
            card.formatted = self.cleaned_data["cardtext"]

        card.save()
        return True
