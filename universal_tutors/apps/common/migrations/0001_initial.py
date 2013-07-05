# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Feedback'
        db.create_table('common_feedback', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question_1', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('question_1_comments', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('question_2', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('question_2_comments', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('question_3', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('question_3_comments', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('question_4', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('question_4_comments', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('common', ['Feedback'])

    def backwards(self, orm):
        # Deleting model 'Feedback'
        db.delete_table('common_feedback')

    models = {
        'common.feedback': {
            'Meta': {'object_name': 'Feedback'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_1': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'question_1_comments': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'question_2': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'question_2_comments': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'question_3': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'question_3_comments': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'question_4': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'question_4_comments': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['common']