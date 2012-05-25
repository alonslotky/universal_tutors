# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'WithdrawItem'
        db.create_table('profile_withdrawitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='withdraws', to=orm['auth.User'])),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(related_name='withdraws', to=orm['core.Currency'])),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('credits', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('status', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('invoice', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal('profile', ['WithdrawItem'])


    def backwards(self, orm):
        
        # Deleting model 'WithdrawItem'
        db.delete_table('profile_withdrawitem')


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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 21, 15, 57, 1, 936450)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 21, 15, 57, 1, 936341)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'classes.class': {
            'Meta': {'ordering': "('status', 'date', 'start')", 'object_name': 'Class'},
            'alert_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cancelation_reason': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'credit_fee': ('django.db.models.fields.FloatField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'earning_fee': ('django.db.models.fields.FloatField', [], {}),
            'end': ('django.db.models.fields.TimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scribblar_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.TimeField', [], {}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'classes_as_student'", 'to': "orm['auth.User']"}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'classes'", 'to': "orm['classes.ClassSubject']"}),
            'tutor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'classes_as_tutor'", 'to': "orm['auth.User']"}),
            'universal_fee': ('django.db.models.fields.FloatField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'classes.classsubject': {
            'Meta': {'object_name': 'ClassSubject'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
        'profile.child': {
            'Meta': {'object_name': 'Child'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'child': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parent_set'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'to': "orm['auth.User']"})
        },
        'profile.dayavailability': {
            'Meta': {'object_name': 'DayAvailability'},
            'begin': ('django.db.models.fields.TimeField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'day_off': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end': ('django.db.models.fields.TimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'day_availability'", 'to': "orm['auth.User']"})
        },
        'profile.message': {
            'Meta': {'ordering': "('created',)", 'object_name': 'Message'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'related_class': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'messages'", 'null': 'True', 'to': "orm['classes.Class']"}),
            'to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'received_messages'", 'to': "orm['auth.User']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sent_messages'", 'to': "orm['auth.User']"})
        },
        'profile.newslettersubscription': {
            'Meta': {'object_name': 'NewsletterSubscription'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            'email_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hash_key': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'profile.referral': {
            'Meta': {'object_name': 'Referral'},
            'activated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'used': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'referrals'", 'to': "orm['auth.User']"})
        },
        'profile.report': {
            'Meta': {'ordering': "('created',)", 'object_name': 'Report'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sent_report'", 'to': "orm['auth.User']"}),
            'violator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'received_report'", 'to': "orm['auth.User']"})
        },
        'profile.studentreview': {
            'Meta': {'object_name': 'StudentReview'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'related_class': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'student_reviews'", 'to': "orm['classes.Class']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reviews_as_student'", 'to': "orm['auth.User']"})
        },
        'profile.topupitem': {
            'Meta': {'ordering': "['-created']", 'object_name': 'TopUpItem'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'credits': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'topups'", 'to': "orm['core.Currency']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'topups'", 'to': "orm['auth.User']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'profile.tutorfavorite': {
            'Meta': {'unique_together': "(('user', 'tutor'),)", 'object_name': 'TutorFavorite'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tutor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'students_has_favorite'", 'to': "orm['auth.User']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'favorite_tutors'", 'to': "orm['auth.User']"})
        },
        'profile.tutorqualification': {
            'Meta': {'object_name': 'TutorQualification'},
            'document': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'qualification': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'qualifications'", 'to': "orm['auth.User']"})
        },
        'profile.tutorreview': {
            'Meta': {'object_name': 'TutorReview'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rate': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'related_class': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tutor_reviews'", 'to': "orm['classes.Class']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reviews_as_tutor'", 'to': "orm['auth.User']"})
        },
        'profile.tutorsubject': {
            'Meta': {'object_name': 'TutorSubject'},
            'credits': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tutors'", 'to': "orm['classes.ClassSubject']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subjects'", 'to': "orm['auth.User']"})
        },
        'profile.usercreditmovement': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'UserCreditMovement'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'credits': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'movements'", 'to': "orm['auth.User']"})
        },
        'profile.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'about': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'activated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'activation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'avg_rate': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'classes_given': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'country': ('apps.common.utils.fields.CountryField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'crb': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'crb_checked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'crb_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'credit': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Currency']", 'null': 'True', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'favorite': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'favorites'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gender': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'income': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'interests': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'students'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['classes.ClassSubject']"}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'max_credits': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'min_credits': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'newsletters': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'no_reviews': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'other_referral': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'paypal_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'profile_image': ('django.db.models.fields.files.ImageField', [], {'default': "'images/defaults/profile.png'", 'max_length': '100'}),
            'referral': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'referral_key': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'scribblar_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'UTC'", 'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'video': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'webcam': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'profile.weekavailability': {
            'Meta': {'object_name': 'WeekAvailability'},
            'begin': ('django.db.models.fields.TimeField', [], {}),
            'end': ('django.db.models.fields.TimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'week_availability'", 'to': "orm['auth.User']"}),
            'weekday': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'profile.withdrawitem': {
            'Meta': {'ordering': "['-created']", 'object_name': 'WithdrawItem'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'credits': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'withdraws'", 'to': "orm['core.Currency']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'withdraws'", 'to': "orm['auth.User']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['profile']
