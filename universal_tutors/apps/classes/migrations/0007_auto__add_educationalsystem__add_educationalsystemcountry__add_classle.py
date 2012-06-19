# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'EducationalSystem'
        db.create_table('classes_educationalsystem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('system', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('classes', ['EducationalSystem'])

        # Adding model 'EducationalSystemCountry'
        db.create_table('classes_educationalsystemcountry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('system', self.gf('django.db.models.fields.related.ForeignKey')(related_name='countries', to=orm['classes.EducationalSystem'])),
            ('country', self.gf('apps.common.utils.fields.CountryField')(max_length=2)),
        ))
        db.send_create_signal('classes', ['EducationalSystemCountry'])

        # Adding model 'ClassLevel'
        db.create_table('classes_classlevel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('system', self.gf('django.db.models.fields.related.ForeignKey')(related_name='levels', to=orm['classes.EducationalSystem'])),
            ('level', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('classes', ['ClassLevel'])

        # Adding model 'EducationalSystemSubject'
        db.create_table('classes_educationalsystemsubject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('system', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subjects', to=orm['classes.EducationalSystem'])),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(related_name='educational_systems', to=orm['classes.ClassSubject'])),
        ))
        db.send_create_signal('classes', ['EducationalSystemSubject'])

        # Changing field 'Class.subject'
        db.alter_column('classes_class', 'subject_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profile.TutorSubject']))


    def backwards(self, orm):
        
        # Deleting model 'EducationalSystem'
        db.delete_table('classes_educationalsystem')

        # Deleting model 'EducationalSystemCountry'
        db.delete_table('classes_educationalsystemcountry')

        # Deleting model 'ClassLevel'
        db.delete_table('classes_classlevel')

        # Deleting model 'EducationalSystemSubject'
        db.delete_table('classes_educationalsystemsubject')

        # Changing field 'Class.subject'
        db.alter_column('classes_class', 'subject_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['classes.ClassSubject']))


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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 15, 13, 4, 40, 831248)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 15, 13, 4, 40, 831147)'}),
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
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '30'})
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
        'classes.educationalsystemsubject': {
            'Meta': {'object_name': 'EducationalSystemSubject'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'educational_systems'", 'to': "orm['classes.ClassSubject']"}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subjects'", 'to': "orm['classes.EducationalSystem']"})
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
