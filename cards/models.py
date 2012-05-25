# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models, transaction
from django import forms


class Category(models.Model):
    title = models.CharField(u"Название", max_length=200)
    slug = models.SlugField()
    has_cards = models.BooleanField(u"Есть статьи", default=False, db_index=True, editable=False)
    sort = models.PositiveIntegerField()

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'Раздел'
        verbose_name_plural = u'Разделы'
        ordering = ['sort']


class Tag(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    title = models.CharField(u"Название", max_length=100)
    slug = models.SlugField()
    has_cards = models.BooleanField(u"Есть статьи", default=False, db_index=True, editable=False)
    sort = models.PositiveIntegerField()

    def __unicode__(self):
        return u'{0} : {1}'.format(self.category.title, self.title)

    class Meta:
        verbose_name = u'Тег'
        verbose_name_plural = u'Теги'
        ordering = ['sort']
        order_with_respect_to = 'category'


class Cards(models.Model):
    topic = models.CharField(u"Название", max_length=140)
    # Исходный текст заметки
    cardtext = models.TextField(u"Заметка")
    # Подсвеченный текст заметки
    formatted = models.TextField(blank=True, editable=False)
    owner = models.ForeignKey(User, verbose_name=u'Добавил', editable=False)
    added = models.DateTimeField(u'Добавлена', auto_now_add=True)
    comments = models.IntegerField(u'Комментариев', default=0, editable=False)
    rating = models.IntegerField(u'Рейтинг заметки', editable=False, default=0)
    tag = models.ForeignKey(Tag, blank=True, null=True, verbose_name=u'Тег', on_delete=models.PROTECT)

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


def category_has_cards_update(sender, instance, **kw):
    """ Определяем категории в которых есть статьи """
    with transaction.commit_on_success():
        Category.objects.all().update(has_cards=False)
        Tag.objects.all().update(has_cards=False)
        tags = set()
        for c in Cards.objects.filter(tag__isnull=False).values('tag_id'):
            tags.add(c['tag_id'])
        Tag.objects.filter(pk__in=tags).update(has_cards=True)
        categories = set()
        for t in Tag.objects.filter(has_cards=True).values('category_id'):
            categories.add(t['category_id'])
        Category.objects.filter(pk__in=categories).update(has_cards=True)
models.signals.post_save.connect(category_has_cards_update, sender=Cards, dispatch_uid='cards.category_has_cards_update')


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
        fields = ( 'tag', 'topic', 'cardtext' )


def format_code(text):
    '''Function to find [code] tags and replace with highlited code'''
    import bbcode
    return bbcode.to_html(text)

