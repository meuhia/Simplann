# coding: utf-8

from django import template

from Simplan.event.models import MakeUserChoice, MakeGuestChoice, OptionFree, \
    OptionTime


register = template.Library()


@register.filter('get_choice_by_user')
def get_choice_by_user(option, user):
    
    try:
        choice = MakeUserChoice.objects.get(choice__option__pk=option.pk, user__pk=user.pk).choice
    except :
        choice = None
    return choice

@register.filter('get_choice_by_username')
def get_choice_by_username(option, username):
    try:
        choice = MakeGuestChoice.objects.get(choice__option__pk=option.pk, username=username).choice
    except :
        choice = None
    return choice

@register.filter('cast_option')
def cast_option(option):
    try:
        option = OptionFree.objects.get(pk=option.pk)
    except :
        try:
            option = OptionTime.objects.get(pk=option.pk)
        except :
            option = None
    
    return option

