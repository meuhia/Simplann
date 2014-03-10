# coding: utf-8

from django import template

from Simplan.account.models import Profile
from django.contrib.auth.models import User


register = template.Library()


@register.filter('profile')
def profile(user):
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
    return profile

@register.filter('user')
def user(pk):
    try:
        user = User.objects.get(pk=pk)
    except:
        user = None
    return user
