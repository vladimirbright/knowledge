# -*- coding: utf8 -*-


from django.contrib.auth.models import User
from django.db import models
from django import forms
from datetime import datetime
import re

# Create your models here.
class UserRegisterForm(forms.Form):
    username = forms.CharField(
                    max_length=35,
                    min_length=3,
                    label=u'Имя пользователя',
                    error_messages = {
                        'required':   u'Без имен пользователей не бывает!',
                        'max_length': u'Слишком длинное имя пользователя, не больше 35 символов',
                        'min_length': u'Слишком короткое имя пользователя, не короче 3 символов'
                        }
                              )

    email   = forms.EmailField(
                    label=u'E-mail',
                    error_messages = {
                        'required': u'Введите e-mail',
                        'invalid' : u'Вы ввели некорректный e-mail'
                        }
                )

    password = forms.CharField(
                    max_length = 35,
                    min_length = 3,
                    label      = u'Пароль',
                    widget     = forms.PasswordInput,
                    error_messages = {
                        'required':   u'Пароль необходим!',
                        'max_length': u'Слишком длинный пароль, не больше 35 символов',
                        'min_length': u'Слишком короткий пароль, не короче 3 символов'
                        }
                )

    passwordconfirm = forms.CharField(
                    max_length  = 35,
                    min_length  = 3,
                    label       = u'Повторите пароль',
                    widget      = forms.PasswordInput,
                    error_messages = {
                        'required':   u'Вы не повторили пароль'
                        }
                )
    # Honey pot, ага
    confirmemail = forms.CharField(
                    label      = u'Confirm email',
                    max_length = 16,
                    initial    = ' '
                )


    def clean_username(self):
        '''Check username'''
        username = self.cleaned_data['username'].strip()

        if username == '':
            raise forms.ValidationError(u'Вы ввели пустое имя пользователя!')

        if re.search(r'[^a-z0-9_]+', username, re.I) is not None:
            raise forms.ValidationError(u'Разрешены только латинские символы, цифры и _')

        # Проверяем есть ли уже юзер с таким именем
        try:
            u = User.objects.get(username__exact=username)
            if u is not None:
                raise forms.ValidationError(u'Пользователь с таким именем уже существует')
        except User.DoesNotExist:
            pass

        return username

    def clean_passwordconfirm(self):
        password = self.cleaned_data['password']
        cpassword = self.cleaned_data['passwordconfirm']
        if password != cpassword:
            raise forms.ValidationError(u'Введенные пароли не совпадают!')

    def clean_confirmemail(self):
        '''Ловим спамеров'''
        s = self.cleaned_data['confirmemail'].strip()
        if s != '':
            raise forms.ValidationError(u'Чертовы спамеры!')
        return s

    def save(self):
        ''' Создаем пользователя '''
        user = User.objects.create_user(
                    self.cleaned_data['username'],
                    self.cleaned_data['email'],
                    self.cleaned_data['password']
                    )

