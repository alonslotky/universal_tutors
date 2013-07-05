# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'FeedbackQuestionOptions'
        db.delete_table('common_feedbackquestionoptions')

        # Adding model 'FeedbackQuestionOption'
        db.create_table('common_feedbackquestionoption', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True, blank=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.FeedbackQuestion'])),
            ('votes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('common', ['FeedbackQuestionOption'])

        # Adding model 'FeedbackQuestionComment'
        db.create_table('common_feedbackquestioncomment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.FeedbackQuestion'])),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('common', ['FeedbackQuestionComment'])


        # Changing field 'Feedback.question_answer'
        db.alter_column('common_feedback', 'question_answer_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.FeedbackQuestionOption']))
    def backwards(self, orm):
        # Adding model 'FeedbackQuestionOptions'
        db.create_table('common_feedbackquestionoptions', (
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.FeedbackQuestion'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('common', ['FeedbackQuestionOptions'])

        # Deleting model 'FeedbackQuestionOption'
        db.delete_table('common_feedbackquestionoption')

        # Deleting model 'FeedbackQuestionComment'
        db.delete_table('common_feedbackquestioncomment')


        # Changing field 'Feedback.question_answer'
        db.alter_column('common_feedback', 'question_answer_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.FeedbackQuestionOptions']))
    models = {
        'common.feedback': {
            'Meta': {'object_name': 'Feedback'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.FeedbackQuestion']"}),
            'question_answer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.FeedbackQuestionOption']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'common.feedbackquestion': {
            'Meta': {'object_name': 'FeedbackQuestion'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'optional_text_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'common.feedbackquestioncomment': {
            'Meta': {'object_name': 'FeedbackQuestionComment'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.FeedbackQuestion']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'common.feedbackquestionoption': {
            'Meta': {'object_name': 'FeedbackQuestionOption'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.FeedbackQuestion']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['common']