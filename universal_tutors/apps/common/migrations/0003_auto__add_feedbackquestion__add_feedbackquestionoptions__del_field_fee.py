# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FeedbackQuestion'
        db.create_table('common_feedbackquestion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True, blank=True)),
            ('optional_text_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('common', ['FeedbackQuestion'])

        # Adding model 'FeedbackQuestionOptions'
        db.create_table('common_feedbackquestionoptions', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True, blank=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.FeedbackQuestion'])),
        ))
        db.send_create_signal('common', ['FeedbackQuestionOptions'])

        # Deleting field 'Feedback.question_3_comments'
        db.delete_column('common_feedback', 'question_3_comments')

        # Deleting field 'Feedback.question_4_comments'
        db.delete_column('common_feedback', 'question_4_comments')

        # Deleting field 'Feedback.question_2_comments'
        db.delete_column('common_feedback', 'question_2_comments')

        # Deleting field 'Feedback.question_3'
        db.delete_column('common_feedback', 'question_3')

        # Deleting field 'Feedback.question_2'
        db.delete_column('common_feedback', 'question_2')

        # Deleting field 'Feedback.question_1'
        db.delete_column('common_feedback', 'question_1')

        # Deleting field 'Feedback.question_4'
        db.delete_column('common_feedback', 'question_4')

        # Deleting field 'Feedback.question_1_comments'
        db.delete_column('common_feedback', 'question_1_comments')

        # Adding field 'Feedback.question'
        db.add_column('common_feedback', 'question',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['common.FeedbackQuestion']),
                      keep_default=False)

        # Adding field 'Feedback.question_answer'
        db.add_column('common_feedback', 'question_answer',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['common.FeedbackQuestionOptions']),
                      keep_default=False)

        # Adding field 'Feedback.comment'
        db.add_column('common_feedback', 'comment',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting model 'FeedbackQuestion'
        db.delete_table('common_feedbackquestion')

        # Deleting model 'FeedbackQuestionOptions'
        db.delete_table('common_feedbackquestionoptions')

        # Adding field 'Feedback.question_3_comments'
        db.add_column('common_feedback', 'question_3_comments',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Feedback.question_4_comments'
        db.add_column('common_feedback', 'question_4_comments',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Feedback.question_2_comments'
        db.add_column('common_feedback', 'question_2_comments',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Feedback.question_3'
        db.add_column('common_feedback', 'question_3',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Feedback.question_2'
        db.add_column('common_feedback', 'question_2',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Feedback.question_1'
        db.add_column('common_feedback', 'question_1',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Feedback.question_4'
        db.add_column('common_feedback', 'question_4',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Feedback.question_1_comments'
        db.add_column('common_feedback', 'question_1_comments',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Feedback.question'
        db.delete_column('common_feedback', 'question_id')

        # Deleting field 'Feedback.question_answer'
        db.delete_column('common_feedback', 'question_answer_id')

        # Deleting field 'Feedback.comment'
        db.delete_column('common_feedback', 'comment')

    models = {
        'common.feedback': {
            'Meta': {'object_name': 'Feedback'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.FeedbackQuestion']"}),
            'question_answer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.FeedbackQuestionOptions']"}),
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
        'common.feedbackquestionoptions': {
            'Meta': {'object_name': 'FeedbackQuestionOptions'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.FeedbackQuestion']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['common']
