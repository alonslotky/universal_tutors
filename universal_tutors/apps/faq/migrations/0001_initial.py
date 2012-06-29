# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'FAQSection'
        db.create_table('faq_faqsection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('section', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('faq', ['FAQSection'])

        # Adding model 'FAQItem'
        db.create_table('faq_faqitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='items', null=True, to=orm['faq.FAQSection'])),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('answers', self.gf('django.db.models.fields.TextField')()),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('faq', ['FAQItem'])


    def backwards(self, orm):
        
        # Deleting model 'FAQSection'
        db.delete_table('faq_faqsection')

        # Deleting model 'FAQItem'
        db.delete_table('faq_faqitem')


    models = {
        'faq.faqitem': {
            'Meta': {'object_name': 'FAQItem'},
            'answers': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'items'", 'null': 'True', 'to': "orm['faq.FAQSection']"})
        },
        'faq.faqsection': {
            'Meta': {'object_name': 'FAQSection'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'section': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['faq']
