# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Feedback.created'
        db.add_column('common_feedback', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2012, 5, 25, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Feedback.updated'
        db.add_column('common_feedback', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2012, 5, 25, 0, 0), blank=True),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'Feedback.created'
        db.delete_column('common_feedback', 'created')

        # Deleting field 'Feedback.updated'
        db.delete_column('common_feedback', 'updated')

    models = {
        'common.feedback': {
            'Meta': {'object_name': 'Feedback'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_1': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'question_1_comments': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'question_2': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'question_2_comments': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'question_3': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'question_3_comments': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'question_4': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'question_4_comments': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['common']