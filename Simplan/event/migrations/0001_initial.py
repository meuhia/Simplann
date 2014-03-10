# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Choice'
        db.create_table(u'event_choice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('positive', self.gf('django.db.models.fields.BooleanField')()),
            ('option', self.gf('django.db.models.fields.related.ForeignKey')(related_name='option_choice', to=orm['event.Option'])),
        ))
        db.send_create_signal(u'event', ['Choice'])

        # Adding model 'Option'
        db.create_table(u'event_option', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('required', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='option_required', null=True, to=orm['event.Choice'])),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='event', to=orm['event.Event'])),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal(u'event', ['Option'])

        # Adding model 'Event'
        db.create_table(u'event_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('place', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('slug_public', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('mailing_list', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'event', ['Event'])

        # Adding model 'EventGuest'
        db.create_table(u'event_eventguest', (
            (u'event_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['event.Event'], unique=True, primary_key=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'event', ['EventGuest'])

        # Adding model 'EventUser'
        db.create_table(u'event_eventuser', (
            (u'event_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['event.Event'], unique=True, primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
        ))
        db.send_create_signal(u'event', ['EventUser'])

        # Adding model 'OptionTime'
        db.create_table(u'event_optiontime', (
            (u'option_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['event.Option'], unique=True, primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'event', ['OptionTime'])

        # Adding model 'OptionFree'
        db.create_table(u'event_optionfree', (
            (u'option_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['event.Option'], unique=True, primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'event', ['OptionFree'])

        # Adding model 'MakeChoice'
        db.create_table(u'event_makechoice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('choice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['event.Choice'])),
        ))
        db.send_create_signal(u'event', ['MakeChoice'])

        # Adding model 'MakeGuestChoice'
        db.create_table(u'event_makeguestchoice', (
            (u'makechoice_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['event.MakeChoice'], unique=True, primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=80)),
        ))
        db.send_create_signal(u'event', ['MakeGuestChoice'])

        # Adding model 'MakeUserChoice'
        db.create_table(u'event_makeuserchoice', (
            (u'makechoice_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['event.MakeChoice'], unique=True, primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'event', ['MakeUserChoice'])


    def backwards(self, orm):
        # Deleting model 'Choice'
        db.delete_table(u'event_choice')

        # Deleting model 'Option'
        db.delete_table(u'event_option')

        # Deleting model 'Event'
        db.delete_table(u'event_event')

        # Deleting model 'EventGuest'
        db.delete_table(u'event_eventguest')

        # Deleting model 'EventUser'
        db.delete_table(u'event_eventuser')

        # Deleting model 'OptionTime'
        db.delete_table(u'event_optiontime')

        # Deleting model 'OptionFree'
        db.delete_table(u'event_optionfree')

        # Deleting model 'MakeChoice'
        db.delete_table(u'event_makechoice')

        # Deleting model 'MakeGuestChoice'
        db.delete_table(u'event_makeguestchoice')

        # Deleting model 'MakeUserChoice'
        db.delete_table(u'event_makeuserchoice')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'event.choice': {
            'Meta': {'object_name': 'Choice'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'option_choice'", 'to': u"orm['event.Option']"}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'positive': ('django.db.models.fields.BooleanField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'event.event': {
            'Meta': {'object_name': 'Event'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mailing_list': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'slug_public': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        u'event.eventguest': {
            'Meta': {'object_name': 'EventGuest', '_ormbases': [u'event.Event']},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'event_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['event.Event']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'event.eventuser': {
            'Meta': {'object_name': 'EventUser', '_ormbases': [u'event.Event']},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            u'event_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['event.Event']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'event.makechoice': {
            'Meta': {'object_name': 'MakeChoice'},
            'choice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['event.Choice']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'event.makeguestchoice': {
            'Meta': {'object_name': 'MakeGuestChoice', '_ormbases': [u'event.MakeChoice']},
            u'makechoice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['event.MakeChoice']", 'unique': 'True', 'primary_key': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        u'event.makeuserchoice': {
            'Meta': {'object_name': 'MakeUserChoice', '_ormbases': [u'event.MakeChoice']},
            u'makechoice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['event.MakeChoice']", 'unique': 'True', 'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'event.option': {
            'Meta': {'ordering': "['position']", 'object_name': 'Option'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'event'", 'to': u"orm['event.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'required': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'option_required'", 'null': 'True', 'to': u"orm['event.Choice']"})
        },
        u'event.optionfree': {
            'Meta': {'ordering': "['position']", 'object_name': 'OptionFree', '_ormbases': [u'event.Option']},
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'option_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['event.Option']", 'unique': 'True', 'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        u'event.optiontime': {
            'Meta': {'ordering': "['position']", 'object_name': 'OptionTime', '_ormbases': [u'event.Option']},
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'option_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['event.Option']", 'unique': 'True', 'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['event']