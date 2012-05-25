# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Feedback'
        db.delete_table('common_feedback')

        # Deleting model 'FeedbackQuestionComment'
        db.delete_table('common_feedbackquestioncomment')

        # Adding model 'FeedbackQuestionAnswer'
        db.create_table('common_feedbackquestionanswer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.FeedbackQuestion'])),
            ('option', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.FeedbackQuestionOption'])),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('common', ['FeedbackQuestionAnswer'])

        # Deleting field 'FeedbackQuestionOption.votes'
        db.delete_column('common_feedbackquestionoption', 'votes')

        # Deleting field 'FeedbackQuestionOption.slug'
        db.delete_column('common_feedbackquestionoption', 'slug')


        # Changing field 'FeedbackQuestionOption.title'
        db.alter_column('common_feedbackquestionoption', 'title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))
    def backwards(self, orm):
        # Adding model 'Feedback'
        db.create_table('common_feedback', (
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.FeedbackQuestion'])),
            ('question_answer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.FeedbackQuestionOption'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('common', ['Feedback'])

        # Adding model 'FeedbackQuestionComment'
        db.create_table('common_feedbackquestioncomment', (
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.FeedbackQuestion'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('common', ['FeedbackQuestionComment'])

        # Deleting model 'FeedbackQuestionAnswer'
        db.delete_table('common_feedbackquestionanswer')

        # Adding field 'FeedbackQuestionOption.votes'
        db.add_column('common_feedbackquestionoption', 'votes',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'FeedbackQuestionOption.slug'
        db.add_column('common_feedbackquestionoption', 'slug',
                      self.gf('django.db.models.fields.SlugField')(max_length=50, null=True, blank=True),
                      keep_default=False)


        # Changing field 'FeedbackQuestionOption.title'
        db.alter_column('common_feedbackquestionoption', 'title', self.gf('django.db.models.fields.CharField')(default='', max_length=200))
    models = {
        'common.feedbackquestion': {
            'Meta': {'object_name': 'FeedbackQuestion'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'optional_text_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'common.feedbackquestionanswer': {
            'Meta': {'object_name': 'FeedbackQuestionAnswer'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.FeedbackQuestionOption']"}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.FeedbackQuestion']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'common.feedbackquestionoption': {
            'Meta': {'object_name': 'FeedbackQuestionOption'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.FeedbackQuestion']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['common']