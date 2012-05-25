# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'MassPayment'
        db.create_table('ap_masspayment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('currency_code', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('sender_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('memo', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
        ))
        db.send_create_signal('ap', ['MassPayment'])

        # Adding model 'MassPaymentReceiver'
        db.create_table('ap_masspaymentreceiver', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('payment', self.gf('django.db.models.fields.related.ForeignKey')(related_name='receivers', to=orm['ap.MassPayment'])),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('primary', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('ap', ['MassPaymentReceiver'])


    def backwards(self, orm):
        
        # Deleting model 'MassPayment'
        db.delete_table('ap_masspayment')

        # Deleting model 'MassPaymentReceiver'
        db.delete_table('ap_masspaymentreceiver')


    models = {
        'ap.masspayment': {
            'Meta': {'object_name': 'MassPayment'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency_code': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memo': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'sender_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
        },
        'ap.masspaymentreceiver': {
            'Meta': {'object_name': 'MassPaymentReceiver'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'receivers'", 'to': "orm['ap.MassPayment']"}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['ap']
