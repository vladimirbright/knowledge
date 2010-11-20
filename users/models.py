# -*- coding: utf-8 -*-

from datetime import datetime
import re

from django.contrib.auth.models import User
from django.db import models
from django import forms


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
                    min_length = 4,
                    label      = u'Пароль',
                    widget     = forms.PasswordInput,
                    error_messages = {
                        'required':   u'Пароль необходим',
                        }
                )

    passwordconfirm = forms.CharField(
                    max_length  = 35,
                    min_length  = 4,
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
        try:
            password = self.cleaned_data['password']
            cpassword = self.cleaned_data['passwordconfirm']
            if password != cpassword:
                raise forms.ValidationError(u'Введенные пароли не совпадают')
        except KeyError:
            raise forms.ValidationError(u'')

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
        user.save()


class UserSettingsForm(forms.Form):
    email   = forms.EmailField(
                    label=u'E-mail',
                    error_messages = {
                        'required': u'Введите e-mail',
                        'invalid' : u'Вы ввели некорректный e-mail'
                        }
                )

    password = forms.CharField(
                    max_length = 35,
                    min_length = 4,
                    label      = u'Пароль',
                    widget     = forms.PasswordInput,
                    required   = False,
                    error_messages = {
                        'required':   u'Пароль необходим',
                        }
                )

    passwordconfirm = forms.CharField(
                    max_length  = 35,
                    min_length  = 4,
                    required   = False,
                    label       = u'Повторите пароль',
                    widget      = forms.PasswordInput,
                    error_messages = {
                        'required':   u'Вы не повторили пароль'
                        }
                )

    def clean_passwordconfirm(self):
        try:
            password = self.cleaned_data['password']
        except KeyError:
            raise forms.ValidationError(u'Введите пароль')
        try:
            cpassword = self.cleaned_data['passwordconfirm']
            if password != cpassword:
                raise forms.ValidationError(u'Введенные пароли не совпадают')
        except KeyError:
            raise forms.ValidationError(u'Повторите пароль')

    def save(self, User):
        ''' UserSettingsForm.save(User) '''
        if self.is_valid():
            try:
                User.email = self.cleaned_data['email']
            except KeyError:
                pass
            try:
                User.set_password(self.cleaned_data['password'])
            except KeyError:
                pass
            User.save()
