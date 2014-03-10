# coding: utf-8

from django.contrib import admin

from .models import EventGuest, EventUser, Choice, OptionTime, OptionFree, MakeGuestChoice, MakeUserChoice 


admin.site.register(EventGuest)
admin.site.register(EventUser)
admin.site.register(Choice)
admin.site.register(OptionTime)
admin.site.register(OptionFree)
admin.site.register(MakeGuestChoice)
admin.site.register(MakeUserChoice)
