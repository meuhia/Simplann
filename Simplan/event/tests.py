# coding: utf-8
from datetime import datetime
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase
import os.path

from Simplan import settings
from Simplan.account.factories import UserFactory
from Simplan.event.factories import EventGuestFactory, EventUserFactory, \
    OptionTimeFactory, OptionFreeFactory, ChoiceFactory
from Simplan.event.models import EventGuest, Event, OptionFree, OptionTime, \
    EventUser, Option, Choice


class EventGuestViewsTests(TestCase):
    def setUp(self):
        self.url = reverse('Simplan.event.views.new_event')
        self.data_guest_event = {'title': u'Réunion de département',
                          'description': u'Réunion mensuelle du département de la chambre de commerce',
                          'place': 'Paris, France',
                          'author': 'stoffelen',
                          'email': 'stoffelen@yahoo.com'}
        
        self.data_user_event = {'title': u'Réunion de département',
                          'description': u'Réunion mensuelle du département de la chambre de commerce',
                          'place': 'Paris, France'}
        
        self.data_free_option = {'text': u'Salle des Fleurs',
                              'image': open(settings.SITE_ROOT +'/fixtures/fleur.jpg', 'r')}
        
        self.data_free_huge_option = {'text': u'Salle des Oiseaux',
                                      'image': open(settings.SITE_ROOT +'/fixtures/birds.jpg', 'r')}
        
        settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
    
    def test_create_guest_event(self):
        '''
        Check create an event by guest
        '''
        
        res = self.client.post(self.url, self.data_guest_event,
                               follow=False)
        #check if post has been executed
        self.assertEqual(res.status_code, 302)
        
        #check that event is in the EventGuest table
        value = EventGuest.objects.get(pk=1)
        
        self.assertEquals(value.title, u'Réunion de département')
        self.assertEquals(value.description, u'Réunion mensuelle du département de la chambre de commerce')
        self.assertEquals(value.place, 'Paris, France')
        self.assertEquals(value.author, 'stoffelen')
        self.assertEquals(value.email, 'stoffelen@yahoo.com')
        
        #check that event is in the Event table
        value = Event.objects.get(pk=1)
        
        self.assertEquals(value.title, u'Réunion de département')
        self.assertEquals(value.description, u'Réunion mensuelle du département de la chambre de commerce')
        self.assertEquals(value.place, 'Paris, France')
    
    def test_create_user_event(self):
        '''
        Check create an event by a user
        '''
        user = UserFactory()
        log = self.client.login(username=user.username, password='1234')
        self.assertEqual(log, True)
        
        res = self.client.post(self.url, self.data_user_event, follow=False)
        #check if post has been executed
        self.assertEqual(res.status_code, 302)
        
        #check that event is in the EventGuest table
        value = EventUser.objects.get(pk=1)
        
        self.assertEquals(value.title, u'Réunion de département')
        self.assertEquals(value.description, u'Réunion mensuelle du département de la chambre de commerce')
        self.assertEquals(value.place, 'Paris, France')
        self.assertEquals(value.author, user)
        
        #check that event is in the Event table
        value = Event.objects.get(pk=1)
        
        self.assertEquals(value.title, u'Réunion de département')
        self.assertEquals(value.description, u'Réunion mensuelle du département de la chambre de commerce')
        self.assertEquals(value.place, 'Paris, France')
        
    def test_add_free_option_for_guest(self):
        '''
        Check a free option which attributes are prerequisites, can be added to a guest event
        '''
        
        egf = EventGuestFactory()
        
        res = self.client.post(reverse('Simplan.event.views.new_option', args=[egf.slug])+'?type=free',
                               self.data_free_option,
                               follow=False)
        #check if post has been executed
        self.assertEqual(res.status_code, 302)
        
        res2 = self.client.post(reverse('Simplan.event.views.new_option', args=[egf.slug])+'?type=free',
                               {'text': u'Salle des Chiens'},
                               follow=False)
        self.assertEqual(res2.status_code, 302)
        
        #add huge image
        res3 = self.client.post(reverse('Simplan.event.views.new_option', args=[egf.slug])+'?type=free', 
                               self.data_free_huge_option,
                               follow=False)
        self.assertEqual(res3.status_code, 404)
        
        #add time option
        otf  = OptionTimeFactory(event=egf, position=3)
        
        res4 = self.client.post(reverse('Simplan.event.views.new_option', args=[egf.slug])+'?type=free',
                               {'text': u'Salle des Ours'},
                               follow=False)
        self.assertEqual(res4.status_code, 302)
        
        #check that row is insert
        self.assertEquals(OptionFree.objects.count(),3)
        self.assertEquals(Option.objects.count(),4)
        
        value1 = OptionFree.objects.get(pk=1)
        value2 = OptionFree.objects.get(pk=2)
        value3 = OptionFree.objects.get(pk=4)
        
        #check position
        self.assertEquals(value1.position, 1)
        self.assertEquals(value2.position, 2)
        self.assertEquals(value3.position, 4)
        
        #check that image has been upload
        self.assertEqual(os.path.isfile(value1.image.path), True)
        #delete temp image
        os.remove(value1.image.path)
        
        #check default choice number
        self.assertEquals(Choice.objects.filter(option__pk=value1.pk).count(),len(settings.SETTING_CHOICES[0]))
        self.assertEquals(Choice.objects.filter(option__pk=value2.pk).count(),len(settings.SETTING_CHOICES[0]))
        self.assertEquals(Choice.objects.filter(option__pk=value3.pk).count(),len(settings.SETTING_CHOICES[0]))
    
    def test_add_free_option_for_user(self):
        '''
        Check a free option which attributes are prerequisites, can be added to a user event
        '''
        user = UserFactory()
        log = self.client.login(username=user.username, password='1234')
        self.assertEqual(log, True)
        
        euf = EventUserFactory(author=user)
        
        res = self.client.post(reverse('Simplan.event.views.new_option', args=[euf.slug])+'?type=free',
                               self.data_free_option,
                               follow=False)
        #check if post has been executed
        self.assertEqual(res.status_code, 302)
        
        res2 = self.client.post(reverse('Simplan.event.views.new_option', args=[euf.slug])+'?type=free',
                               {'text': u'Salle des Chiens'},
                               follow=False)
        self.assertEqual(res2.status_code, 302)
        
        #add huge image
        res3 = self.client.post(reverse('Simplan.event.views.new_option', args=[euf.slug])+'?type=free', 
                               self.data_free_huge_option,
                               follow=False)
        self.assertEqual(res3.status_code, 404)
        
        #add time option
        otf  = OptionTimeFactory(event=euf, position=3)
        
        res4 = self.client.post(reverse('Simplan.event.views.new_option', args=[euf.slug])+'?type=free',
                               {'text': u'Salle des Ours'},
                               follow=False)
        self.assertEqual(res4.status_code, 302)
        
        #check that row is insert
        self.assertEquals(OptionFree.objects.count(),3)
        self.assertEquals(Option.objects.count(),4)
        
        value1 = OptionFree.objects.get(pk=1)
        value2 = OptionFree.objects.get(pk=2)
        value3 = OptionFree.objects.get(pk=4)
        
        #check position
        self.assertEquals(value1.position, 1)
        self.assertEquals(value2.position, 2)
        self.assertEquals(value3.position, 4)
        
        #check that image has been upload
        self.assertEqual(os.path.isfile(value1.image.path), True)
        #delete temp image
        os.remove(value1.image.path)
        
        self.client.logout()
        
        #check default choice number
        self.assertEquals(Choice.objects.filter(option__pk=value1.pk).count(),len(settings.SETTING_CHOICES[0]))
        self.assertEquals(Choice.objects.filter(option__pk=value2.pk).count(),len(settings.SETTING_CHOICES[0]))
        self.assertEquals(Choice.objects.filter(option__pk=value3.pk).count(),len(settings.SETTING_CHOICES[0]))
    
    def test_add_time_option_for_guest(self):
        egf = EventGuestFactory()
        res = self.client.post(reverse('Simplan.event.views.new_option', args=[egf.slug])+'?type=time', 
                               {'date': datetime.now()},
                               follow=False)
        self.assertEqual(res.status_code, 302)
        
        res2 = self.client.post(reverse('Simplan.event.views.new_option', args=[egf.slug])+'?type=time', 
                               {'date': datetime.now()},
                               follow=False)
        self.assertEqual(res.status_code, 302)
        
        #add time option
        off  = OptionFreeFactory(event=egf, position=3)
        
        res3 = self.client.post(reverse('Simplan.event.views.new_option', args=[egf.slug])+'?type=time', 
                               {'date': datetime.now()},
                               follow=False)
        self.assertEqual(res.status_code, 302)
        
        #check that an option has been insert
        self.assertEquals(OptionTime.objects.count(),3)
        self.assertEquals(Option.objects.count(),4)
        
        value1 = OptionTime.objects.get(pk=1)
        value2 = OptionTime.objects.get(pk=2)
        value3 = OptionTime.objects.get(pk=4)
        
        #check position
        self.assertEquals(value1.position, 1)
        self.assertEquals(value2.position, 2)
        self.assertEquals(value3.position, 4)
        
        #check default choice number
        self.assertEquals(Choice.objects.filter(option__pk=value1.pk).count(),len(settings.SETTING_CHOICES[0]))
        self.assertEquals(Choice.objects.filter(option__pk=value2.pk).count(),len(settings.SETTING_CHOICES[0]))
        self.assertEquals(Choice.objects.filter(option__pk=value3.pk).count(),len(settings.SETTING_CHOICES[0]))
    
    def test_add_time_option_for_user(self):
        user = UserFactory()
        log = self.client.login(username=user.username, password='1234')
        self.assertEqual(log, True)
        
        euf = EventUserFactory()
        res = self.client.post(reverse('Simplan.event.views.new_option', args=[euf.slug])+'?type=time', 
                               {'date': datetime.now()},
                               follow=False)
        self.assertEqual(res.status_code, 302)
        
        res2 = self.client.post(reverse('Simplan.event.views.new_option', args=[euf.slug]), 
                               {'date': datetime.now()},
                               follow=False)
        self.assertEqual(res.status_code, 302)
        
        #add time option
        off  = OptionFreeFactory(event=euf, position=3)
        
        res3 = self.client.post(reverse('Simplan.event.views.new_option', args=[euf.slug])+'?type=time', 
                               {'date': datetime.now()},
                               follow=False)
        self.assertEqual(res.status_code, 302)
        
        #check that an option has been insert
        self.assertEquals(OptionTime.objects.count(),3)
        self.assertEquals(Option.objects.count(),4)
        
        value1 = OptionTime.objects.get(pk=1)
        value2 = OptionTime.objects.get(pk=2)
        value3 = OptionTime.objects.get(pk=4)
        
        #check position
        self.assertEquals(value1.position, 1)
        self.assertEquals(value2.position, 2)
        self.assertEquals(value3.position, 4)
        
        #check default choice number
        self.assertEquals(Choice.objects.filter(option__pk=value1.pk).count(),len(settings.SETTING_CHOICES[0]))
        self.assertEquals(Choice.objects.filter(option__pk=value2.pk).count(),len(settings.SETTING_CHOICES[0]))
        self.assertEquals(Choice.objects.filter(option__pk=value3.pk).count(),len(settings.SETTING_CHOICES[0]))
    
    def test_edit_time_option_for_guest(self):
        
        egf = EventGuestFactory()
        otf1  = OptionTimeFactory(event=egf, position=1)
        otf2  = OptionTimeFactory(event=egf, position=2)
        otf3  = OptionTimeFactory(event=egf, position=3)
        
        res = self.client.post(reverse('Simplan.event.views.edit_option', args=[otf2.pk])+'?type=time', 
                               {'date': datetime(2015, 1, 1, 0, 0)},
                               follow=False)
        
        self.assertEqual(res.status_code, 302)
        
        #check that no option has been insert
        self.assertEquals(OptionTime.objects.count(),3)
        
        value1 = OptionTime.objects.get(pk=1)
        value2 = OptionTime.objects.get(pk=2)
        value3 = OptionTime.objects.get(pk=3)
        
        #check that option has been update
        self.assertEquals(value2.start_date, datetime(2015, 1, 1, 0, 0))
        
        #check position
        self.assertEquals(value1.position, 1)
        self.assertEquals(value2.position, 2)
        self.assertEquals(value3.position, 3)
    
    def test_edit_time_option_for_user(self):
        
        user = UserFactory()
        log = self.client.login(username=user.username, password='1234')
        self.assertEqual(log, True)
        
        euf = EventUserFactory()
        otf1  = OptionTimeFactory(event=euf, position=1)
        otf2  = OptionTimeFactory(event=euf, position=2)
        otf3  = OptionTimeFactory(event=euf, position=3)
        
        res = self.client.post(reverse('Simplan.event.views.edit_option', args=[otf2.pk])+'?type=time', 
                               {'date': datetime(2015, 1, 1, 0, 0)},
                               follow=False)
        
        self.assertEqual(res.status_code, 302)
        
        #check that no option has been insert
        self.assertEquals(OptionTime.objects.count(),3)
        
        value1 = OptionTime.objects.get(pk=1)
        value2 = OptionTime.objects.get(pk=2)
        value3 = OptionTime.objects.get(pk=3)
        
        #check that option has been update
        self.assertEquals(value2.start_date, datetime(2015, 1, 1, 0, 0))
        
        #check position
        self.assertEquals(value1.position, 1)
        self.assertEquals(value2.position, 2)
        self.assertEquals(value3.position, 3)
    
    def test_edit_free_option_for_guest(self):
        
        egf = EventGuestFactory()
        off1  = OptionFreeFactory(event=egf, position=1)
        off2  = OptionFreeFactory(event=egf, position=2)
        off3  = OptionFreeFactory(event=egf, position=3)
        
        res = self.client.post(reverse('Simplan.event.views.edit_option', args=[off2.pk])+'?type=free', 
                               {'text': u'Toilettes'},
                               follow=False)
        
        self.assertEqual(res.status_code, 302)
        
        #check that no option has been insert
        self.assertEquals(OptionFree.objects.count(),3)
        
        value1 = OptionFree.objects.get(pk=1)
        value2 = OptionFree.objects.get(pk=2)
        value3 = OptionFree.objects.get(pk=3)
        
        #check that option has been update
        self.assertEquals(value2.text, u'Toilettes')
        
        #check position
        self.assertEquals(value1.position, 1)
        self.assertEquals(value2.position, 2)
        self.assertEquals(value3.position, 3)
    
    def test_edit_free_option_for_user(self):
        
        user = UserFactory()
        log = self.client.login(username=user.username, password='1234')
        self.assertEqual(log, True)
        
        euf = EventUserFactory()
        off1  = OptionFreeFactory(event=euf, position=1)
        off2  = OptionFreeFactory(event=euf, position=2)
        off3  = OptionFreeFactory(event=euf, position=3)
        
        res = self.client.post(reverse('Simplan.event.views.edit_option', args=[off2.pk])+'?type=free', 
                               {'text': u'Toilettes'},
                               follow=False)
        
        self.assertEqual(res.status_code, 302)
        
        #check that no option has been insert
        self.assertEquals(OptionFree.objects.count(),3)
        
        value1 = OptionFree.objects.get(pk=1)
        value2 = OptionFree.objects.get(pk=2)
        value3 = OptionFree.objects.get(pk=3)
        
        #check that option has been update
        self.assertEquals(value2.text, u'Toilettes')
        
        #check position
        self.assertEquals(value1.position, 1)
        self.assertEquals(value2.position, 2)
        self.assertEquals(value3.position, 3)
    
    def test_delete_time_option_for_guest(self):
        
        egf = EventGuestFactory()
        otf1  = OptionTimeFactory(event=egf, position=1)
        otf2  = OptionTimeFactory(event=egf, position=2)
        off1  = OptionFreeFactory(event=egf, position=3)
        otf3  = OptionTimeFactory(event=egf, position=4)
        
        res = self.client.get(reverse('Simplan.event.views.del_option', args=[otf2.pk])+'?type=time',
                               follow=False)
        self.assertEqual(res.status_code, 302)
        
        #check that option has been deleted
        self.assertEquals(OptionTime.objects.count(),2)
        self.assertEquals(OptionFree.objects.count(),1)
        self.assertEquals(Option.objects.count(),3)
        
        #check position
        self.assertEquals(Option.objects.get(pk=1).position, 1)
        self.assertEquals(Option.objects.get(pk=3).position, 3)
        self.assertEquals(Option.objects.get(pk=4).position, 4)
        
        #try to remove an inexistant option
        res = self.client.get(reverse('Simplan.event.views.del_option', args=[otf2.pk])+'?type=time',
                               follow=False)
        self.assertEqual(res.status_code, 404)
    
    def test_delete_time_option_for_user(self):
        
        user = UserFactory()
        log = self.client.login(username=user.username, password='1234')
        self.assertEqual(log, True)
        
        euf = EventUserFactory()
        otf1  = OptionTimeFactory(event=euf, position=1)
        otf2  = OptionTimeFactory(event=euf, position=2)
        off1  = OptionFreeFactory(event=euf, position=3)
        otf3  = OptionTimeFactory(event=euf, position=4)
        
        res = self.client.get(reverse('Simplan.event.views.del_option', args=[otf2.pk]),
                               follow=False)
        self.assertEqual(res.status_code, 302)
        
        #check that option has been deleted
        self.assertEquals(OptionTime.objects.count(),2)
        self.assertEquals(OptionFree.objects.count(),1)
        self.assertEquals(Option.objects.count(),3)
        
        #check position
        self.assertEquals(Option.objects.get(pk=1).position, 1)
        self.assertEquals(Option.objects.get(pk=3).position, 3)
        self.assertEquals(Option.objects.get(pk=4).position, 4)
        
        #try to remove an inexistant option
        res = self.client.get(reverse('Simplan.event.views.del_option', args=[otf2.pk]),
                               follow=False)
        self.assertEqual(res.status_code, 404)
    
    def test_delete_free_option_for_guest(self):
        
        egf = EventGuestFactory()
        otf1  = OptionFreeFactory(event=egf, position=1)
        otf2  = OptionFreeFactory(event=egf, position=2)
        off1  = OptionTimeFactory(event=egf, position=3)
        otf3  = OptionFreeFactory(event=egf, position=4)
        
        res = self.client.get(reverse('Simplan.event.views.del_option', args=[otf2.pk]),
                               follow=False)
        self.assertEqual(res.status_code, 302)
        
        #check that option has been deleted
        self.assertEquals(OptionTime.objects.count(),1)
        self.assertEquals(OptionFree.objects.count(),2)
        self.assertEquals(Option.objects.count(),3)
        
        #check position
        self.assertEquals(Option.objects.get(pk=1).position, 1)
        self.assertEquals(Option.objects.get(pk=3).position, 3)
        self.assertEquals(Option.objects.get(pk=4).position, 4)
        
        #try to remove an inexistant option
        res = self.client.get(reverse('Simplan.event.views.del_option', args=[otf2.pk]),
                               follow=False)
        self.assertEqual(res.status_code, 404)
    
    def test_delete_free_option_for_user(self):
        
        user = UserFactory()
        log = self.client.login(username=user.username, password='1234')
        self.assertEqual(log, True)
        
        euf = EventUserFactory()
        otf1  = OptionFreeFactory(event=euf, position=1)
        otf2  = OptionFreeFactory(event=euf, position=2)
        off1  = OptionTimeFactory(event=euf, position=3)
        otf3  = OptionFreeFactory(event=euf, position=4)
        
        res = self.client.get(reverse('Simplan.event.views.del_option', args=[otf2.pk]),
                               follow=False)
        self.assertEqual(res.status_code, 302)
        
        #check that option has been deleted
        self.assertEquals(OptionTime.objects.count(),1)
        self.assertEquals(OptionFree.objects.count(),2)
        self.assertEquals(Option.objects.count(),3)
        
        #check position
        self.assertEquals(Option.objects.get(pk=1).position, 1)
        self.assertEquals(Option.objects.get(pk=3).position, 3)
        self.assertEquals(Option.objects.get(pk=4).position, 4)
        
        #try to remove an inexistant option
        res = self.client.get(reverse('Simplan.event.views.del_option', args=[otf2.pk]),
                               follow=False)
        self.assertEqual(res.status_code, 404)
    
    def test_down_free_option_for_guest(self):
        
        egf = EventGuestFactory()
        otf1  = OptionTimeFactory(event=egf, position=1)
        otf2  = OptionFreeFactory(event=egf, position=2)
        otf3  = OptionTimeFactory(event=egf, position=5)
        otf4  = OptionTimeFactory(event=egf, position=7)
        
        old2 = otf2.position
        old3 = otf3.position
        
        res = self.client.get(reverse('Simplan.event.views.down_option', args=[otf2.pk]),follow=False)
        self.assertEqual(res.status_code, 302)
        
        #check that option has been deleted
        self.assertEquals(OptionTime.objects.count(),3)
        
        value2 = OptionFree.objects.get(pk=otf2.pk)
        value3 = OptionTime.objects.get(pk=otf3.pk)
        
        self.assertEquals(value2.position, old3)
        self.assertEquals(value3.position, old2)
        
        res = self.client.get(reverse('Simplan.event.views.down_option', args=[otf1.pk]),follow=False)
        self.assertEqual(res.status_code, 302)
        
        res = self.client.get(reverse('Simplan.event.views.down_option', args=[otf4.pk]),follow=False)
        self.assertEqual(res.status_code, 404)
    
    def test_up_option_for_guest(self):
        
        egf = EventGuestFactory()
        otf1  = OptionTimeFactory(event=egf, position=1)
        otf2  = OptionFreeFactory(event=egf, position=2)
        otf3  = OptionTimeFactory(event=egf, position=5)
        otf4  = OptionTimeFactory(event=egf, position=7)
        
        old2 = otf2.position
        old3 = otf3.position
        
        res = self.client.get(reverse('Simplan.event.views.up_option', args=[otf3.pk]),follow=False)
        self.assertEqual(res.status_code, 302)
        
        #check option's number
        self.assertEquals(OptionTime.objects.count(),3)
        
        value2 = OptionFree.objects.get(pk=otf2.pk)
        value3 = OptionTime.objects.get(pk=otf3.pk)
        
        self.assertEquals(value2.position, old3)
        self.assertEquals(value3.position, old2)
        
        res = self.client.get(reverse('Simplan.event.views.up_option', args=[otf1.pk]),follow=False)
        self.assertEqual(res.status_code, 404)
        
        res = self.client.get(reverse('Simplan.event.views.up_option', args=[otf4.pk]),follow=False)
        self.assertEqual(res.status_code, 302)
    
    def test_down_free_option_for_user(self):
        
        user = UserFactory()
        log = self.client.login(username=user.username, password='1234')
        self.assertEqual(log, True)
        
        euf = EventUserFactory()
        otf1  = OptionTimeFactory(event=euf, position=1)
        otf2  = OptionFreeFactory(event=euf, position=2)
        otf3  = OptionTimeFactory(event=euf, position=5)
        otf4  = OptionTimeFactory(event=euf, position=7)
        
        old2 = otf2.position
        old3 = otf3.position
        
        res = self.client.get(reverse('Simplan.event.views.down_option', args=[otf2.pk]),follow=False)
        self.assertEqual(res.status_code, 302)
        
        #check option's number
        self.assertEquals(OptionTime.objects.count(),3)
        
        value2 = OptionFree.objects.get(pk=otf2.pk)
        value3 = OptionTime.objects.get(pk=otf3.pk)
        
        self.assertEquals(value2.position, old3)
        self.assertEquals(value3.position, old2)
        
        res = self.client.get(reverse('Simplan.event.views.down_option', args=[otf1.pk]),follow=False)
        self.assertEqual(res.status_code, 302)
        
        res = self.client.get(reverse('Simplan.event.views.down_option', args=[otf4.pk]),follow=False)
        self.assertEqual(res.status_code, 404)
    
    def test_up_option_for_user(self):
        
        user = UserFactory()
        log = self.client.login(username=user.username, password='1234')
        self.assertEqual(log, True)
        
        euf = EventUserFactory()
        otf1  = OptionTimeFactory(event=euf, position=1)
        otf2  = OptionFreeFactory(event=euf, position=2)
        otf3  = OptionTimeFactory(event=euf, position=5)
        otf4  = OptionTimeFactory(event=euf, position=7)
        
        old2 = otf2.position
        old3 = otf3.position
        
        res = self.client.get(reverse('Simplan.event.views.up_option', args=[otf3.pk]),follow=False)
        self.assertEqual(res.status_code, 302)
        
        #check that option has been deleted
        self.assertEquals(OptionTime.objects.count(),3)
        
        value2 = OptionFree.objects.get(pk=otf2.pk)
        value3 = OptionTime.objects.get(pk=otf3.pk)
        
        self.assertEquals(value2.position, old3)
        self.assertEquals(value3.position, old2)
        
        res = self.client.get(reverse('Simplan.event.views.up_option', args=[otf1.pk]),follow=False)
        self.assertEqual(res.status_code, 404)
        
        res = self.client.get(reverse('Simplan.event.views.up_option', args=[otf4.pk]),follow=False)
        self.assertEqual(res.status_code, 302)
        
    def test_add_choice_for_guest(self):
        egf = EventGuestFactory()
        
        off1  = OptionFreeFactory(event=egf, position=1)
        off2  = OptionFreeFactory(event=egf, position=2)
        otf1  = OptionTimeFactory(event=egf, position=5)
        off3  = OptionFreeFactory(event=egf, position=7)
        
        
        res = self.client.post(reverse('Simplan.event.views.new_choice', args=[off1.pk]),
                               {'title': u'Oui','description': u'Oh oui',},
                               follow=False)
        
        self.assertEqual(res.status_code, 302)
        
        #check choice has been created
        self.assertEquals(Choice.objects.filter(option__pk=off1.pk).count(),1)
        self.assertEquals(Choice.objects.filter(option__pk=off2.pk).count(),0)
        self.assertEquals(Choice.objects.filter(option__pk=off3.pk).count(),0)
        self.assertEquals(Choice.objects.filter(option__pk=otf1.pk).count(),0)
        
        res = self.client.post(reverse('Simplan.event.views.new_choice', args=[off1.pk]),
                               {'title': u'Non','description': u'Out boy',},
                               follow=False)
        
        self.assertEqual(res.status_code, 302)
        
        #check choice has been created
        self.assertEquals(Choice.objects.filter(option__pk=off1.pk).count(),2)
        self.assertEquals(Choice.objects.filter(option__pk=off2.pk).count(),0)
        self.assertEquals(Choice.objects.filter(option__pk=off3.pk).count(),0)
        self.assertEquals(Choice.objects.filter(option__pk=otf1.pk).count(),0)
    
    def test_add_choice_for_user(self):
        user = UserFactory()
        log = self.client.login(username=user.username, password='1234')
        self.assertEqual(log, True)
        
        euf = EventUserFactory()
        off1  = OptionFreeFactory(event=euf, position=1)
        off2  = OptionFreeFactory(event=euf, position=2)
        otf1  = OptionTimeFactory(event=euf, position=5)
        off3  = OptionFreeFactory(event=euf, position=7)
        
        
        res = self.client.post(reverse('Simplan.event.views.new_choice', args=[off1.pk]),
                               {'title': u'Oui','description': u'Oh oui',},
                               follow=False)
        
        self.assertEqual(res.status_code, 302)
        
        #check choice has been created
        self.assertEquals(Choice.objects.filter(option__pk=off1.pk).count(),1)
        self.assertEquals(Choice.objects.filter(option__pk=off2.pk).count(),0)
        self.assertEquals(Choice.objects.filter(option__pk=off3.pk).count(),0)
        self.assertEquals(Choice.objects.filter(option__pk=otf1.pk).count(),0)
        
        res = self.client.post(reverse('Simplan.event.views.new_choice', args=[off1.pk]),
                               {'title': u'Non','description': u'Out boy',},
                               follow=False)
        
        self.assertEqual(res.status_code, 302)
        
        #check choice has been created
        self.assertEquals(Choice.objects.filter(option__pk=off1.pk).count(),2)
        self.assertEquals(Choice.objects.filter(option__pk=off2.pk).count(),0)
        self.assertEquals(Choice.objects.filter(option__pk=off3.pk).count(),0)
        self.assertEquals(Choice.objects.filter(option__pk=otf1.pk).count(),0)
    
    def test_modify_choice_for_guest(self):
        egf = EventGuestFactory()
        
        off1  = OptionFreeFactory(event=egf, position=1)
        off2  = OptionFreeFactory(event=egf, position=2)
        otf1  = OptionTimeFactory(event=egf, position=5)
        off3  = OptionFreeFactory(event=egf, position=7)
        
        
        res = self.client.post(reverse('Simplan.event.views.modify_choice'),
                               {'option_pk': str(off1.pk), 'choice_title': u'Oui','choice_positive': 'check','choice_add':'valider'},
                               follow=False)
        
        self.assertEqual(res.status_code, 302)
        
        #check choice has been created
        self.assertEquals(Choice.objects.filter(option__pk=off1.pk).count(),1)
        self.assertEquals(Choice.objects.filter(option__pk=off2.pk).count(),0)
        self.assertEquals(Choice.objects.filter(option__pk=off3.pk).count(),0)
        self.assertEquals(Choice.objects.filter(option__pk=otf1.pk).count(),0)
        
        res = self.client.post(reverse('Simplan.event.views.modify_choice'),
                               {'option_pk': str(off1.pk), 'choice_title': u'Non','choice_add':'valider'},
                               follow=False)
        self.assertEqual(res.status_code, 302)
        
        #check choice has been created
        self.assertEquals(Choice.objects.filter(option__pk=off1.pk).count(),2)
        self.assertEquals(Choice.objects.filter(option__pk=off2.pk).count(),0)
        self.assertEquals(Choice.objects.filter(option__pk=off3.pk).count(),0)
        self.assertEquals(Choice.objects.filter(option__pk=otf1.pk).count(),0)
        
        res = self.client.post(reverse('Simplan.event.views.modify_choice'),
                               {'option_pk': str(off2.pk), 'choice_title': u'Oui','choice_positive': 'check','choice_add':'valider'},
                               follow=False)
        self.assertEqual(res.status_code, 302)
        
        res = self.client.post(reverse('Simplan.event.views.modify_choice'),
                               {'option_pk': str(off2.pk), 'choice_title': u'Non','choice_add':'valider'},
                               follow=False)
        self.assertEqual(res.status_code, 302)
        
        #check choice has been created
        self.assertEquals(Choice.objects.filter(option__pk=off1.pk).count(),2)
        self.assertEquals(Choice.objects.filter(option__pk=off2.pk).count(),2)
        self.assertEquals(Choice.objects.filter(option__pk=off3.pk).count(),0)
        self.assertEquals(Choice.objects.filter(option__pk=otf1.pk).count(),0)
        
        res = self.client.post(reverse('Simplan.event.views.modify_choice'),
                               {'option_pk': str(otf1.pk), 'choice_title': u'Oui','choice_positive': 'check','choice_add':'valider'},
                               follow=False)
        self.assertEqual(res.status_code, 302)
        
        #check choice has been created
        self.assertEquals(Choice.objects.filter(option__pk=off1.pk).count(),2)
        self.assertEquals(Choice.objects.filter(option__pk=off2.pk).count(),2)
        self.assertEquals(Choice.objects.filter(option__pk=off3.pk).count(),0)
        self.assertEquals(Choice.objects.filter(option__pk=otf1.pk).count(),1)
        
        res = self.client.post(reverse('Simplan.event.views.modify_choice'),
                               {'choice_pk': '3', 'choice_title': u'Probablement','choice_maj':'valider'},
                               follow=False)
        self.assertEqual(res.status_code, 302)
        
        #check choice has been updated
        self.assertEquals(Choice.objects.filter(option__pk=off1.pk).count(),2)
        self.assertEquals(Choice.objects.filter(option__pk=off2.pk).count(),2)
        self.assertEquals(Choice.objects.filter(option__pk=off3.pk).count(),0)
        self.assertEquals(Choice.objects.filter(option__pk=otf1.pk).count(),1)
        
        #check global values
        self.assertEquals(Choice.objects.get(pk=1).title,'Oui')
        self.assertEquals(Choice.objects.get(pk=1).positive, True)
        self.assertEquals(Choice.objects.get(pk=2).title,'Non')
        self.assertEquals(Choice.objects.get(pk=2).positive, False)
        self.assertEquals(Choice.objects.get(pk=3).title,'Probablement')
        self.assertEquals(Choice.objects.get(pk=3).positive, False)
        self.assertEquals(Choice.objects.get(pk=4).title,'Non')
        self.assertEquals(Choice.objects.get(pk=4).positive, False)
        self.assertEquals(Choice.objects.get(pk=5).title,'Oui')
        self.assertEquals(Choice.objects.get(pk=5).positive, True)
        
        res = self.client.post(reverse('Simplan.event.views.modify_choice'),
                               {'event_pk': egf.pk, 'choice_title': u'Peut-être','choice_positive':'check', 'answer_add':'valider'},
                               follow=False)
        self.assertEqual(res.status_code, 302)
        
        #check choice has been created
        self.assertEquals(Choice.objects.filter(option__pk=off1.pk).count(),3)
        self.assertEquals(Choice.objects.filter(option__pk=off2.pk).count(),3)
        self.assertEquals(Choice.objects.filter(option__pk=off3.pk).count(),1)
        self.assertEquals(Choice.objects.filter(option__pk=otf1.pk).count(),2)
        
        #check global values
        self.assertEquals(Choice.objects.get(pk=6).title,u'Peut-être')
        self.assertEquals(Choice.objects.get(pk=6).positive, True)
        self.assertEquals(Choice.objects.get(pk=7).title,u'Peut-être')
        self.assertEquals(Choice.objects.get(pk=7).positive, True)
        self.assertEquals(Choice.objects.get(pk=8).title,u'Peut-être')
        self.assertEquals(Choice.objects.get(pk=8).positive, True)
        self.assertEquals(Choice.objects.get(pk=9).title,u'Peut-être')
        self.assertEquals(Choice.objects.get(pk=9).positive, True)
    
    def test_modify_choice_for_user(self):
        user = UserFactory()
        log = self.client.login(username=user.username, password='1234')
        self.assertEqual(log, True)
        
        euf = EventUserFactory()
        
        off1  = OptionFreeFactory(event=euf, position=1)
        off2  = OptionFreeFactory(event=euf, position=2)
        otf1  = OptionTimeFactory(event=euf, position=5)
        off3  = OptionFreeFactory(event=euf, position=7)
        
        
        res = self.client.post(reverse('Simplan.event.views.modify_choice'),
                               {'option_pk': str(off1.pk), 'choice_title': u'Oui','choice_positive': 'check','choice_add':'valider'},
                               follow=False)
        
        self.assertEqual(res.status_code, 302)
        
        #check choice has been created
        self.assertEquals(Choice.objects.filter(option__pk=off1.pk).count(),1)
        self.assertEquals(Choice.objects.filter(option__pk=off2.pk).count(),0)
        self.assertEquals(Choice.objects.filter(option__pk=off3.pk).count(),0)
        self.assertEquals(Choice.objects.filter(option__pk=otf1.pk).count(),0)
        
        res = self.client.post(reverse('Simplan.event.views.modify_choice'),
                               {'option_pk': str(off1.pk), 'choice_title': u'Non','choice_add':'valider'},
                               follow=False)
        self.assertEqual(res.status_code, 302)
        
        #check choice has been created
        self.assertEquals(Choice.objects.filter(option__pk=off1.pk).count(),2)
        self.assertEquals(Choice.objects.filter(option__pk=off2.pk).count(),0)
        self.assertEquals(Choice.objects.filter(option__pk=off3.pk).count(),0)
        self.assertEquals(Choice.objects.filter(option__pk=otf1.pk).count(),0)
        
        res = self.client.post(reverse('Simplan.event.views.modify_choice'),
                               {'option_pk': str(off2.pk), 'choice_title': u'Oui','choice_positive': 'check','choice_add':'valider'},
                               follow=False)
        self.assertEqual(res.status_code, 302)
        
        res = self.client.post(reverse('Simplan.event.views.modify_choice'),
                               {'option_pk': str(off2.pk), 'choice_title': u'Non','choice_add':'valider'},
                               follow=False)
        self.assertEqual(res.status_code, 302)
        
        #check choice has been created
        self.assertEquals(Choice.objects.filter(option__pk=off1.pk).count(),2)
        self.assertEquals(Choice.objects.filter(option__pk=off2.pk).count(),2)
        self.assertEquals(Choice.objects.filter(option__pk=off3.pk).count(),0)
        self.assertEquals(Choice.objects.filter(option__pk=otf1.pk).count(),0)
        
        res = self.client.post(reverse('Simplan.event.views.modify_choice'),
                               {'option_pk': str(otf1.pk), 'choice_title': u'Oui','choice_positive': 'check','choice_add':'valider'},
                               follow=False)
        self.assertEqual(res.status_code, 302)
        
        #check choice has been created
        self.assertEquals(Choice.objects.filter(option__pk=off1.pk).count(),2)
        self.assertEquals(Choice.objects.filter(option__pk=off2.pk).count(),2)
        self.assertEquals(Choice.objects.filter(option__pk=off3.pk).count(),0)
        self.assertEquals(Choice.objects.filter(option__pk=otf1.pk).count(),1)
        
        res = self.client.post(reverse('Simplan.event.views.modify_choice'),
                               {'choice_pk': '3', 'choice_title': u'Probablement','choice_maj':'valider'},
                               follow=False)
        self.assertEqual(res.status_code, 302)
        
        #check choice has been updated
        self.assertEquals(Choice.objects.filter(option__pk=off1.pk).count(),2)
        self.assertEquals(Choice.objects.filter(option__pk=off2.pk).count(),2)
        self.assertEquals(Choice.objects.filter(option__pk=off3.pk).count(),0)
        self.assertEquals(Choice.objects.filter(option__pk=otf1.pk).count(),1)
        
        #check global values
        self.assertEquals(Choice.objects.get(pk=1).title,'Oui')
        self.assertEquals(Choice.objects.get(pk=1).positive, True)
        self.assertEquals(Choice.objects.get(pk=2).title,'Non')
        self.assertEquals(Choice.objects.get(pk=2).positive, False)
        self.assertEquals(Choice.objects.get(pk=3).title,'Probablement')
        self.assertEquals(Choice.objects.get(pk=3).positive, False)
        self.assertEquals(Choice.objects.get(pk=4).title,'Non')
        self.assertEquals(Choice.objects.get(pk=4).positive, False)
        self.assertEquals(Choice.objects.get(pk=5).title,'Oui')
        self.assertEquals(Choice.objects.get(pk=5).positive, True)
        
        res = self.client.post(reverse('Simplan.event.views.modify_choice'),
                               {'event_pk': euf.pk, 'choice_title': u'Peut-être','choice_positive':'check', 'answer_add':'valider'},
                               follow=False)
        self.assertEqual(res.status_code, 302)
        
        #check choice has been created
        self.assertEquals(Choice.objects.filter(option__pk=off1.pk).count(),3)
        self.assertEquals(Choice.objects.filter(option__pk=off2.pk).count(),3)
        self.assertEquals(Choice.objects.filter(option__pk=off3.pk).count(),1)
        self.assertEquals(Choice.objects.filter(option__pk=otf1.pk).count(),2)
        
        #check global values
        self.assertEquals(Choice.objects.get(pk=6).title,u'Peut-être')
        self.assertEquals(Choice.objects.get(pk=6).positive, True)
        self.assertEquals(Choice.objects.get(pk=7).title,u'Peut-être')
        self.assertEquals(Choice.objects.get(pk=7).positive, True)
        self.assertEquals(Choice.objects.get(pk=8).title,u'Peut-être')
        self.assertEquals(Choice.objects.get(pk=8).positive, True)
        self.assertEquals(Choice.objects.get(pk=9).title,u'Peut-être')
        self.assertEquals(Choice.objects.get(pk=9).positive, True)
    
    
    def test_delete_choice_for_guest(self):
        
        egf = EventGuestFactory()
        
        off1  = OptionFreeFactory(event=egf, position=1)
        off2  = OptionFreeFactory(event=egf, position=2)
        otf1  = OptionTimeFactory(event=egf, position=5)
        off3  = OptionFreeFactory(event=egf, position=7)
        
        cf1_1 = ChoiceFactory(option=off1, position=1)
        cf1_2 = ChoiceFactory(option=off1, position=2)
        cf1_3 = ChoiceFactory(option=off1, position=3)
        cf2_1 = ChoiceFactory(option=off2, position=1)
        cf2_2 = ChoiceFactory(option=off2, position=2)
        cf2_3 = ChoiceFactory(option=off2, position=3)
        cf3_1 = ChoiceFactory(option=otf1, position=1)
        cf3_2 = ChoiceFactory(option=otf1, position=2)
        cf3_3 = ChoiceFactory(option=otf1, position=3)
        
        res = self.client.get(reverse('Simplan.event.views.del_choice', args=[cf2_3.pk]),follow=False)
        self.assertEqual(res.status_code, 302)
        res = self.client.get(reverse('Simplan.event.views.del_choice', args=[cf3_2.pk]),follow=False)
        self.assertEqual(res.status_code, 302)
        res = self.client.get(reverse('Simplan.event.views.del_choice', args=[999]),follow=False)
        self.assertEqual(res.status_code, 404)
        
        #check choice has been deleted
        self.assertEquals(Choice.objects.filter(option__pk=off1.pk).count(),3)
        self.assertEquals(Choice.objects.filter(option__pk=off2.pk).count(),2)
        self.assertEquals(Choice.objects.filter(option__pk=off3.pk).count(),0)
        self.assertEquals(Choice.objects.filter(option__pk=otf1.pk).count(),2)
    
    def test_delete_choice_for_user(self):
        
        user = UserFactory()
        log = self.client.login(username=user.username, password='1234')
        self.assertEqual(log, True)
        
        euf = EventUserFactory()
        
        off1  = OptionFreeFactory(event=euf, position=1)
        off2  = OptionFreeFactory(event=euf, position=2)
        otf1  = OptionTimeFactory(event=euf, position=5)
        off3  = OptionFreeFactory(event=euf, position=7)
        
        cf1_1 = ChoiceFactory(option=off1, position=1)
        cf1_2 = ChoiceFactory(option=off1, position=2)
        cf1_3 = ChoiceFactory(option=off1, position=3)
        cf2_1 = ChoiceFactory(option=off2, position=1)
        cf2_2 = ChoiceFactory(option=off2, position=2)
        cf2_3 = ChoiceFactory(option=off2, position=3)
        cf3_1 = ChoiceFactory(option=otf1, position=1)
        cf3_2 = ChoiceFactory(option=otf1, position=2)
        cf3_3 = ChoiceFactory(option=otf1, position=3)
        
        res = self.client.get(reverse('Simplan.event.views.del_choice', args=[cf2_3.pk]),follow=False)
        self.assertEqual(res.status_code, 302)
        res = self.client.get(reverse('Simplan.event.views.del_choice', args=[cf3_2.pk]),follow=False)
        self.assertEqual(res.status_code, 302)
        res = self.client.get(reverse('Simplan.event.views.del_choice', args=[999]),follow=False)
        self.assertEqual(res.status_code, 404)
        
        #check choice has been deleted
        self.assertEquals(Choice.objects.filter(option__pk=off1.pk).count(),3)
        self.assertEquals(Choice.objects.filter(option__pk=off2.pk).count(),2)
        self.assertEquals(Choice.objects.filter(option__pk=off3.pk).count(),0)
        self.assertEquals(Choice.objects.filter(option__pk=otf1.pk).count(),2)
    
    def test_end_event_for_guest(self):
        egf = EventGuestFactory()
        
        res = self.client.get(reverse('Simplan.event.views.invit_end_event', args=[egf.slug]),follow=False)
        self.assertEqual(res.status_code, 302)
        
        self.assertEquals(len(mail.outbox), 3)
        self.assertEquals(mail.outbox[0].subject, "Simplan - Lien du sondage : "+egf.title)
        self.assertEquals(mail.outbox[0].from_email, 'Simplan <noreply@simplann.eu>')
        self.assertEquals(mail.outbox[0].to, [egf.email.encode('utf-8')])
        
        self.assertEquals(mail.outbox[1].subject, "Simplan - Participez au Sondage : "+egf.title)
        self.assertEquals(mail.outbox[1].from_email, 'Simplan <noreply@simplann.eu>')
        self.assertEquals(mail.outbox[1].to, [egf.mailing_list.split(',')[0].encode('utf-8')])
        
        self.assertEquals(mail.outbox[2].subject, "Simplan - Participez au Sondage : "+egf.title)
        self.assertEquals(mail.outbox[2].from_email, 'Simplan <noreply@simplann.eu>')
        self.assertEquals(mail.outbox[2].to, [egf.mailing_list.split(',')[1].encode('utf-8')])
        
    def test_end_event_for_user(self):
        #TODO
        self.assertEqual(0, 0)

    def test_make_choice_for_guest(self):
        #TODO
        self.assertEqual(0, 0)

    def test_make_choice_for_user(self):
        #TODO
        self.assertEqual(0, 0)
    