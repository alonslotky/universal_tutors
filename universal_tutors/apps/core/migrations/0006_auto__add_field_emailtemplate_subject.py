# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'EmailTemplate.subject'
        db.add_column('core_emailtemplate', 'subject',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'EmailTemplate.subject'
        db.delete_column('core_emailtemplate', 'subject')

    models = {
        'core.bundle': {
            'Meta': {'ordering': "('credits',)", 'object_name': 'Bundle'},
            'credits': ('django.db.models.fields.FloatField', [], {}),
            'discount': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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