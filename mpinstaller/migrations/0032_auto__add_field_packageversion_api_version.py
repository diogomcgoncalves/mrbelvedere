# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PackageVersion.api_version'
        db.add_column(u'mpinstaller_packageversion', 'api_version',
                      self.gf('django.db.models.fields.CharField')(max_length=4, blank=True, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'PackageVersion.api_version'
        db.delete_column(u'mpinstaller_packageversion', 'api_version')


    models = {
        u'mpinstaller.actioneditpicklist': {
            'Meta': {'object_name': 'ActionEditPicklist', '_ormbases': [u'mpinstaller.OrgAction']},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'custom_field': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'custom_object': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'orgaction_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': u"orm['mpinstaller.OrgAction']", 'unique': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'mpinstaller.actioneditstagename': {
            'Meta': {'object_name': 'ActionEditStageName', '_ormbases': [u'mpinstaller.OrgAction']},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'custom_field': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'custom_object': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'forecast_category': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            u'orgaction_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': u"orm['mpinstaller.OrgAction']", 'unique': 'True'}),
            'probability': ('django.db.models.fields.IntegerField', [], {}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'won': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'mpinstaller.installationerror': {
            'Meta': {'object_name': 'InstallationError'},
            'content': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mpinstaller.InstallationErrorContent']", 'null': 'True', 'blank': 'True', 'related_name': "'errors'"}),
            'fallback_content': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mpinstaller.InstallationErrorContent']", 'null': 'True', 'blank': 'True', 'related_name': "'errors_fallback'"}),
            'hide_from_report': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {})
        },
        u'mpinstaller.installationerrorcontent': {
            'Meta': {'object_name': 'InstallationErrorContent'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resolution': ('tinymce.models.HTMLField', [], {})
        },
        u'mpinstaller.metadatacondition': {
            'Meta': {'object_name': 'MetadataCondition'},
            'exclude_namespaces': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'field': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True', 'null': 'True'}),
            'no_match': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'search': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'mpinstaller.orgaction': {
            'Meta': {'object_name': 'OrgAction'},
            'content_failure': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'content_intro': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'content_success': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'force_sandbox': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'mpinstaller.package': {
            'Meta': {'ordering': "['namespace']", 'object_name': 'Package'},
            'content_failure': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'content_failure_beta': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'content_intro': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'content_intro_beta': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'content_success': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'content_success_beta': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'current_beta': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mpinstaller.PackageVersion']", 'null': 'True', 'blank': 'True', 'related_name': "'current_beta'"}),
            'current_github': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mpinstaller.PackageVersion']", 'null': 'True', 'blank': 'True', 'related_name': "'current_github'"}),
            'current_prod': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mpinstaller.PackageVersion']", 'null': 'True', 'blank': 'True', 'related_name': "'current_prod'"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'force_sandbox': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'namespace': ('django.db.models.fields.SlugField', [], {'max_length': '128'}),
            'whitelist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mpinstaller.WhiteList']", 'null': 'True', 'blank': 'True', 'related_name': "'packages'"})
        },
        u'mpinstaller.packageinstallation': {
            'Meta': {'ordering': "['-created']", 'object_name': 'PackageInstallation'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fork': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True', 'null': 'True'}),
            'git_ref': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'install_map': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'instance_url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'log': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'org_id': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'org_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'installations'", 'to': u"orm['mpinstaller.Package']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mpinstaller.PackageVersion']", 'null': 'True', 'blank': 'True', 'related_name': "'installations'"})
        },
        u'mpinstaller.packageinstallationsession': {
            'Meta': {'object_name': 'PackageInstallationSession'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'installation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sessions'", 'to': u"orm['mpinstaller.PackageInstallation']"}),
            'metadata': ('django.db.models.fields.TextField', [], {}),
            'oauth': ('django.db.models.fields.TextField', [], {}),
            'org_packages': ('django.db.models.fields.TextField', [], {})
        },
        u'mpinstaller.packageinstallationstep': {
            'Meta': {'ordering': "['-installation__id', 'order']", 'object_name': 'PackageInstallationStep'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'error': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mpinstaller.InstallationError']", 'null': 'True', 'blank': 'True', 'related_name': "'steps'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'installation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'steps'", 'to': u"orm['mpinstaller.PackageInstallation']"}),
            'log': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mpinstaller.Package']", 'null': 'True', 'blank': 'True', 'related_name': "'installation_steps'"}),
            'previous_version': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True', 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mpinstaller.PackageVersion']", 'null': 'True', 'blank': 'True', 'related_name': "'installation_steps'"})
        },
        u'mpinstaller.packageversion': {
            'Meta': {'ordering': "['package__namespace', 'number']", 'object_name': 'PackageVersion'},
            'api_version': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True', 'null': 'True'}),
            'branch': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True', 'null': 'True'}),
            'conditions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['mpinstaller.MetadataCondition']", 'null': 'True', 'blank': 'True', 'symmetrical': 'False'}),
            'content_failure': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'content_intro': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'content_success': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'github_password': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True', 'null': 'True'}),
            'github_username': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'namespace': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True', 'null': 'True'}),
            'namespace_token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True', 'null': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True', 'null': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'versions'", 'to': u"orm['mpinstaller.Package']"}),
            'package_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True', 'null': 'True'}),
            'repo_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True', 'null': 'True'}),
            'subfolder': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True', 'null': 'True'}),
            'zip_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True', 'null': 'True'})
        },
        u'mpinstaller.packageversiondependency': {
            'Meta': {'ordering': "['order']", 'object_name': 'PackageVersionDependency'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mpinstaller.OrgAction']", 'null': 'True', 'blank': 'True', 'related_name': "'required_by'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'requires': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mpinstaller.PackageVersion']", 'null': 'True', 'blank': 'True', 'related_name': "'required_by'"}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dependencies'", 'to': u"orm['mpinstaller.PackageVersion']"})
        },
        u'mpinstaller.whitelist': {
            'Meta': {'object_name': 'WhiteList'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'mpinstaller.whitelistorg': {
            'Meta': {'object_name': 'WhiteListOrg'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'org_id': ('django.db.models.fields.CharField', [], {'max_length': '18'}),
            'whitelist': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orgs'", 'to': u"orm['mpinstaller.WhiteList']"})
        }
    }

    complete_apps = ['mpinstaller']
