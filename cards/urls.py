# -*- coding: utf8 -*-
# Файло с урл для cards


from django.conf.urls.defaults import *
from knowledge.cards.views import  new_card

urlpatterns = patterns('',
    (r'new/', new_card),
)


