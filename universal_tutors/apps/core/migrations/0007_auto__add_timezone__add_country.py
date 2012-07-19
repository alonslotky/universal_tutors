# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Timezone'
        db.create_table('core_timezone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timezone', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100, db_index=True)),
        ))
        db.send_create_signal('core', ['Timezone'])

        # Adding model 'Country'
        db.create_table('core_country', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('apps.common.utils.fields.CountryField')(unique=True, max_length=2, db_index=True)),
        ))
        db.send_create_signal('core', ['Country'])

        # Adding M2M table for field timezones on 'Country'
        db.create_table('core_country_timezones', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('country', models.ForeignKey(orm['core.country'], null=False)),
            ('timezone', models.ForeignKey(orm['core.timezone'], null=False))
        ))
        db.create_unique('core_country_timezones', ['country_id', 'timezone_id'])


    def backwards(self, orm):
        
        # Deleting model 'Timezone'
        db.delete_table('core_timezone')

        # Deleting model 'Country'
        db.delete_table('core_country')

        # Removing M2M table for field timezones on 'Country'
        db.delete_table('core_country_timezones')


    models = {
        'core.bundle': {
            'Meta': {'ordering': "('credits',)", 'object_name': 'Bundle'},
            'credits': ('django.db.models.fields.FloatField', [], {}),
            'discount': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'core.country': {
            'Meta': {'object_name': 'Country'},
            'country': ('apps.common.utils.fields.CountryField', [], {'unique': 'True', 'max_length': '2', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timezones': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Timezone']", 'symmetrical': 'False'})
        },
        'core.currency': {
            'Meta': {'object_name': 'Currency'},
            'acronym': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manual': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'core.emailtemplate': {
            'Meta': {'object_name': 'EmailTemplate'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True', 'db_index': 'True'})
        },
        'core.quote': {
            'Meta': {'object_name': 'Quote'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quote': ('django.db.models.fields.TextField', [], {})
        },
        'core.timezone': {
            'Meta': {'object_name': 'Timezone'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        },
        'core.video': {
            'Meta': {'object_name': 'Video'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['core']
