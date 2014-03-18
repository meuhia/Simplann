# coding: utf-8

from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase

from Simplan.account.factories import *
from Simplan.event.factories import *

from .models import Profile, TokenRegister


class AccountTests(TestCase):
    
    def setUp(self):
        settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
        
    
    def test_login(self):
        '''
        To test user login
        '''
        user = UserFactory(username='meuhia', password='1234')
        
        result = self.client.post(
                        reverse('Simplan.account.views.login_view'), 
                        {'username': 'meuhia', 'password': '****', 'remember': 'remember'},
                        follow=False)
        #bad password then no redirection
        self.assertEqual(result.status_code, 200)
        
        result = self.client.post(
                        reverse('Simplan.account.views.login_view'), 
                        {'username': 'meuhia','password': '1234','remember': 'remember'},
                        follow=False)
        #good password then redirection
        self.assertEqual(result.status_code, 302)
        
    
    def test_register(self):
        '''
        To test user registration
        '''
        
        result = self.client.post(
                        reverse('Simplan.account.views.register_view'), 
                        {'username': 'meuhia', 'password': '1234', 'password_confirm': '1234', 'email': 'meuhia@simplann.com'},
                        follow=False)
        
        self.assertEqual(result.status_code, 200)
        
        #check email has been sent
        self.assertEquals(len(mail.outbox), 1)
        
        #clic on the link which has been sent in mail
        user = User.objects.get(username='meuhia')
        self.assertEquals(user.is_active, False)
                          
        token = TokenRegister.objects.get(user=user)
        
        result = self.client.get(
                        reverse('Simplan.account.views.active_account')+'?token='+token.token,
                        follow=False)
        self.assertEqual(result.status_code, 200)
        
        self.assertEquals(User.objects.get(username='meuhia').is_active, True)
    
    def test_plans_views(self):
        user = UserFactory()
        profile = ProfileFactory(user=user)
        log = self.client.login(username=user.username, password='1234')
        self.assertEqual(log, True)
        
        #views without plans
        result = self.client.get(
                        reverse('Simplan.account.views.plans'),
                        follow=True)
        self.assertEqual(result.status_code, 200)
        
        #create first event
        euf1 = EventUserFactory(author=user)
        
        off1 = OptionFreeFactory(event=euf1, position=1)
        otf1 = OptionTimeFactory(event=euf1, position=2)
        
        cf1_1 = ChoiceFactory(option=off1, position=1)
        cf1_2 = ChoiceFactory(option=off1, position=2)
        cf2_1 = ChoiceFactory(option=otf1, position=1)
        cf2_2 = ChoiceFactory(option=otf1, position=2)
        
        #views with one plans
        result = self.client.get(
                        reverse('Simplan.account.views.plans'),
                        follow=True)
        self.assertEqual(result.status_code, 200)
        
        #create second event
        euf2 = EventUserFactory(author=user)
        
        off2 = OptionFreeFactory(event=euf2, position=1)
        otf2 = OptionTimeFactory(event=euf2, position=2)
        
        cf3_1 = ChoiceFactory(option=off2, position=1)
        cf3_2 = ChoiceFactory(option=off2, position=2)
        cf4_1 = ChoiceFactory(option=otf2, position=1)
        cf4_2 = ChoiceFactory(option=otf2, position=2)
        
        #views with two plans
        result = self.client.get(
                        reverse('Simplan.account.views.plans'),
                        follow=True)
        self.assertEqual(result.status_code, 200)
        
        
        