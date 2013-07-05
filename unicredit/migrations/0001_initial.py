# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'UnicreditTransactionLog'
        db.create_table('unicredit_unicredittransactionlog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('order_number', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('datacreazione', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('numeroCommerciante', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('stabilimento', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('numeroOrdine', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('statoprecedente', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('statoattuale', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('descrizione', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('unicredit', ['UnicreditTransactionLog'])


    def backwards(self, orm):
        
        # Deleting model 'UnicreditTransactionLog'
        db.delete_table('unicredit_unicredittransactionlog')


    models = {
        'unicredit.unicredittransactionlog': {
            'Meta': {'object_name': 'UnicreditTransactionLog'},
            'datacreazione': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'descrizione': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numeroCommerciante': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'numeroOrdine': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'order_number': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'stabilimento': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'statoattuale': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'statoprecedente': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['unicredit']
