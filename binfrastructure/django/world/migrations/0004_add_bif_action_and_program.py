# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BIFProgram'
        db.create_table('world_bifprogram', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('world', ['BIFProgram'])

        # Adding field 'BIFAction.program'
        db.add_column('world_bifaction', 'program',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='instructions', null=True, to=orm['world.BIFProgram']),
                      keep_default=False)

        # Adding field 'BIFAction.instruction_number'
        db.add_column('world_bifaction', 'instruction_number',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'BIFProgram'
        db.delete_table('world_bifprogram')

        # Deleting field 'BIFAction.program'
        db.delete_column('world_bifaction', 'program_id')

        # Deleting field 'BIFAction.instruction_number'
        db.delete_column('world_bifaction', 'instruction_number')


    models = {
        'world.bifaction': {
            'Meta': {'object_name': 'BIFAction'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instruction_number': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'params': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'program': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'instructions'", 'null': 'True', 'to': "orm['world.BIFProgram']"})
        },
        'world.bifprogram': {
            'Meta': {'object_name': 'BIFProgram'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'world.bin': {
            'Meta': {'object_name': 'Bin'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_empty': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bins'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['world.BinLocation']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'pose_last_seen': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['world.Pose']", 'null': 'True'}),
            'time_last_seen': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        'world.binlocation': {
            'Meta': {'object_name': 'BinLocation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'pickup_dropoff_pose': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['world.Pose']", 'unique': 'True'})
        },
        'world.pose': {
            'Meta': {'object_name': 'Pose'},
            'angle': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'x': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'y': ('django.db.models.fields.FloatField', [], {'default': '0'})
        }
    }

    complete_apps = ['world']