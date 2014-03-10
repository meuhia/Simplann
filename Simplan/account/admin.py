# coding: utf-8

from django.contrib import admin

from .models import Profile, TokenForgotPassword, TokenRegister


admin.site.register(Profile)
admin.site.register(TokenForgotPassword)
admin.site.register(TokenRegister)
