# coding: utf-8

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

from Simplan.event.models import EventUser, MakeUserChoice


class Profile(models.Model):

    '''Represents an user profile'''
    
    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profils'

    user = models.ForeignKey(User, unique=True, verbose_name='Utilisateur')

    id_facebook = models.CharField('Identifiant Facebook', \
                                   max_length=128, blank=True, null=True)
    id_twitter = models.CharField('Identifiant Twitter', max_length=128, blank=True, null=True)
    id_gplus = models.CharField('Identifiant Google Plus', max_length=128, blank=True, null=True)
    avatar_url = models.CharField('URL de l\'avatar', max_length=128, null=True, blank=True)
    
    
    def get_events(self):
        return EventUser.objects.filter(author__pk=self.user.pk).all()
    
    def get_participate_events(self):
        return MakeUserChoice.objects.filter(user__pk=self.user.pk).values_list('choice__option__event__pk',flat=True).distinct().all()
    
    def __unicode__(self):
        '''Textual profile'''
        return u"{0}".format(self.user.username)
        
class TokenForgotPassword(models.Model):
    class Meta:
        verbose_name = 'Token de Mot de passe'
        verbose_name_plural = 'Tokens de Mots de passe'

    user = models.ForeignKey(User, verbose_name='Utilisateur')
    token = models.CharField(max_length=100)
    date_end = models.DateTimeField('Date de fin')

    def get_absolute_url(self):
        '''Absolute URL to the new password page'''
        
        return reverse('Simplan.account.views.new_password')+'?token={0}'.format(self.token)
    def __unicode__(self):
        '''Textual token forgot password'''
        return u"{0} - {1}".format(self.user.username, self.date_end)

class TokenRegister(models.Model):
    class Meta:
        verbose_name = 'Token d\'inscription'
        verbose_name_plural = 'Tokens  d\'inscriptions'

    user = models.ForeignKey(User, verbose_name='Utilisateur')
    token = models.CharField(max_length=100)
    date_end = models.DateTimeField('Date de fin')

    def get_absolute_url(self):
        '''Absolute URL to the active account page'''
        return reverse('Simplan.account.views.active_account')+'?token={0}'.format(self.token)
    
    def __unicode__(self):
        '''Textual token register'''
        return u"{0} - {1}".format(self.user.username, self.date_end)
