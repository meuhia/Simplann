# coding: utf-8

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
import os
import string
import uuid
from django.utils.translation import ugettext_lazy as _

from Simplan import settings


def image_path(instance, filename):
    '''Return path to an image'''
    ext = filename.split('.')[-1]
    filename = u'{}.{}'.format(str(uuid.uuid4()), string.lower(ext))
    return os.path.join('evt', str(instance.pk), filename)

class Choice(models.Model):
    '''Represents a choice'''
    
    class Meta:
        verbose_name = 'Choix'
        verbose_name_plural = 'Choix'
    
    title = models.CharField(max_length=20, verbose_name=_(u"Titre du choix"))
    description = models.TextField(blank=True, verbose_name=_(u"Description du choix"))
    position = models.IntegerField(default=1, verbose_name=_(u"Position"))
    positive = models.BooleanField(verbose_name=_(u"Choix positif"))
    option = models.ForeignKey('Option', verbose_name=_(u"Option du choix"), related_name='option_choice')
    
    def get_makechoice_count(self):
        return MakeChoice.objects.filter(choice__pk=self.pk).count()
    
    
    def __unicode__(self):
        '''Textual forum of an event'''
        if self.positive:
            return u'{0} ({1})+'.format(self.option,self.title)
        else:
            return u'{0} ({1})-'.format(self.option,self.title)

class Option(models.Model):
    '''Represents an option'''
    
    class Meta:
        verbose_name = 'Option'
        verbose_name_plural = 'Options'
        ordering = ['position']
        
    required = models.ForeignKey('Choice',verbose_name=_(u"Choix requis"), related_name='option_required', null=True, blank=True)
    event = models.ForeignKey('Event', verbose_name=_(u"Evenement de l'option"), related_name='event')
    position = models.IntegerField(verbose_name=_(u"Position"), default = 1)
    
    def get_choices(self):
        return Choice.objects.filter(option__pk=self.pk).order_by('position').all()

    def next_free_position(self):
        try:
            return (Choice.objects.filter(option__pk=self.pk).latest('position').position)+1
        except:
            return 1
    
    def __unicode__(self):
        
        try :
            opt = OptionTime.objects.get(pk=self.pk)
            return u'{0}'.format(opt.start_date)
        except:
            opt = OptionFree.objects.get(pk=self.pk)
            return u'{0}'.format(opt.text)
            
    def get_makechoice_positive_count(self):
        return MakeChoice.objects.filter(choice__positive=True, choice__option__pk=self.pk).count()
            
        
class Event(models.Model):
    
    '''Represents an event'''
    
    class Meta:
        verbose_name = 'Evenement'
        verbose_name_plural = 'Evenements'

    title = models.CharField(verbose_name=_(u"Titre de l'évenement"), max_length=80)
    description = models.TextField(verbose_name=_(u"Description"), blank=True, null=True)
    place = models.CharField(verbose_name=_(u"Lieu de l'évenement"), max_length=128, blank=True, null=True)
    slug = models.CharField(verbose_name=_(u"Slug"), max_length=80)
    slug_public = models.CharField(verbose_name=_(u"Slug public"), max_length=80)
    mailing_list = models.TextField(verbose_name=_(u"Liste de diffusion"), blank=True, null=True)
    
    def get_absolute_url(self):
        return settings.SITE_URL+reverse('Simplan.event.views.view_event', args=[
            self.slug_public[0:8], self.slug_public[9:13], self.slug_public[14:18], self.slug_public[19:23], self.slug_public[24:36]
        ])
    
    def get_absolute_admin_url(self):
        return settings.SITE_URL+reverse('Simplan.event.views.recap_event', args=[
            self.slug
        ])
    
    def __unicode__(self):
        '''Textual forum of an event'''
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug :
            self.slug = str(uuid.uuid4())
            self.slug_public = str(uuid.uuid4())
                            
        super(Event, self).save(*args, **kwargs)
    
    def get_max_position(self):
        return Option.objects.filter(event__pk=self.pk).latest('position').position
        
    def next_free_position(self):
        try:
            last = Option.objects.filter(event__pk=self.pk).latest('position')
        except:
            last = None
            
        if last != None:
            return (last.position)+1
        else:
            return 1
    
    def get_options(self):
        
        return Option.objects.filter(event__pk=self.pk).all()
    
    def get_free_options(self):
        
        return OptionFree.objects.filter(event__pk=self.pk).all()
    
    def get_time_options(self):
        
        return OptionTime.objects.filter(event__pk=self.pk).all()
    
    def get_count_options(self):
        self.get_free_options() + self.get_time_options()
    
    def get_participants(self):
        ''' 
        return list of user or guest who participates at event 
        '''
        mucs = MakeUserChoice.objects.filter(choice__option__event__pk = self.pk)
        mgcs = MakeGuestChoice.objects.filter(choice__option__event__pk = self.pk)
        
        retu = []
        retg = []
        for muc in mucs:
            if not muc.user in retu:
                retu.append(muc.user)
        for mgc in mgcs:
            if not mgc.username in retg:
                retg.append(mgc.username)
        
        return {'member': retu, 'guest':retg}

    
    def get_max_mc_positive(self):
        max = 0
        
        for option in self.get_free_options() :
            temp =option.get_makechoice_positive_count() 
            if  temp > max : max = temp
        for option in self.get_time_options() :
            temp =option.get_makechoice_positive_count() 
            if  temp > max : max = temp
        
        return max

class EventGuest(Event):
    '''Represents an event by guest'''
    
    class Meta:
        verbose_name = 'Evenement d\'un invité'
        verbose_name_plural = 'Evenements d\'un invité'
    
    author = models.CharField(verbose_name=_(u"Auteur de l'évenement"), max_length=256)
    email = models.CharField(verbose_name=_(u"Email de l'auteur"), max_length=256)
    
    
class EventUser(Event):
    '''Represents an event by user'''
    
    class Meta:
        verbose_name = 'Evenement d\'un utilisateur'
        verbose_name_plural = 'Evenements d\'un utilisateur'
        
    author = models.ForeignKey(User, verbose_name=_(u"Auteur de l'évènement"), null=True, blank=True)


class OptionTime(Option):
    '''Represents a time option'''
    
    class Meta:
        verbose_name = 'Option de Temps'
        verbose_name_plural = 'Options de Temps'
    
    start_date = models.DateTimeField(verbose_name=_(u"Date de début"))
    end_date = models.DateTimeField(verbose_name=_(u"Date de fin"), null=True, blank=True)
    
    def __unicode__(self):
        '''Textual forum of an option time'''
        return u'{0}:{1}'.format(self.event, self.start_date)

class OptionFree(Option):
    '''Represents a free option'''
    
    class Meta:
        verbose_name = 'Option Libre'
        verbose_name_plural = 'Options Libre'
    
    text = models.CharField(verbose_name=_(u"Texte"), max_length=120)
    image = models.ImageField(upload_to=image_path, verbose_name=_(u"Illustration"), null=True, blank=True)
    
    def __unicode__(self):
        '''Textual forum of an option free'''
        return u'{0}:{1}'.format(self.event, self.text)

class MakeChoice(models.Model):
    '''Represents an choice by user'''
    
    class Meta:
        verbose_name = 'Choix d\'un utilisateur'
        verbose_name_plural = 'Choix d\'un utilisateur'

    choice = models.ForeignKey(Choice, verbose_name=_(u"Choix de l'utilisateur"))
    
class MakeGuestChoice(MakeChoice):
    '''Represents a choice by guest'''
    
    class Meta:
        verbose_name = 'Choix d\'un invité'
        verbose_name_plural = 'Choix d\'un invité'
    
    username = models.CharField(verbose_name=_(u"Pseudo du votant"),  max_length=80)
    
    def __unicode__(self):
        '''Textual MakeGuestChoice'''
        return self.username+' --> '+self.choice.title+ ' pour '+str(self.choice.option)

class MakeUserChoice(MakeChoice):
    '''Represents a choice by registered user'''
    
    class Meta:
        verbose_name = 'Choix d\'un membre'
        verbose_name_plural = 'Choix d\'un membre'
    
    user = models.ForeignKey(User, verbose_name=_(u"Membre votant"))
    
    def __unicode__(self):
        '''Textual MakeUserChoice'''
        return self.user.username+' --> '+self.choice.title+ ' pour '+str(self.choice.option)
    
    
    
