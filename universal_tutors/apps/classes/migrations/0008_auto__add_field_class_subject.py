# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Class.subject'
        db.add_column('classes_class', 'subject', self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='classes', to=orm['profile.TutorSubject']), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Class.subject'
        db.delete_column('classes_class', 'subject_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 19, 10, 22, 23, 867323)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 19, 10, 22, 23, 867150)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'classes.class': {
            'Meta': {'ordering': "('status', 'date')", 'object_name': 'Class'},
            'alert_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cancelation_reason': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'credit_fee': ('django.db.models.fields.FloatField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'duration': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'earning_fee': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scribblar_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'classes_as_student'", 'to': "orm['auth.User']"}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'classes'", 'to': "orm['profile.TutorSubject']"}),
            'tutor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'classes_as_tutor'", 'to': "orm['auth.User']"}),
            'universal_fee': ('django.db.models.fields.FloatField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'classes.classlevel': {
            'Meta': {'object_name': 'ClassLevel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'levels'", 'to': "orm['classes.EducationalSystem']"})
        },
        'classes.classsubject': {
            'Meta': {'object_name': 'ClassSubject'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'systems': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'subjects'", 'symmetrical': 'False', 'to': "orm['classes.EducationalSystem']"})
        },
        'classes.classuserhistory': {
            'Meta': {'object_name': 'ClassUserHistory'},
            '_class': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'history'", 'to': "orm['classes.Class']"}),
            'enter': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leave': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'class_history'", 'to': "orm['auth.User']"})
        },
        'classes.educationalsystem': {
            'Meta': {'object_name': 'EducationalSystem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'system': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'classes.educationalsystemcountry': {
            'Meta': {'object_name': 'EducationalSystemCountry'},
            'country': ('apps.common.utils.fields.CountryField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'countries'", 'to': "orm['classes.EducationalSystem']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'profile.tutorsubject': {
            'Meta': {'object_name': 'TutorSubject'},
            'credits': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tutors'", 'to': "orm['classes.ClassLevel']"}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tutors'", 'to': "orm['classes.ClassSubject']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subjects'", 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['classes']
