# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Deleting model 'Entity'
        db.delete_table('semantic_blog_entity')

        # Removing M2M table for field tags on 'Entity'
        db.delete_table('semantic_blog_entity_tags')

        # Adding M2M table for field tags on 'Article'
        db.create_table('semantic_blog_article_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True,
                                    auto_created=True)),
            ('article',
             models.ForeignKey(orm['semantic_blog.article'], null=False)),
            ('tag', models.ForeignKey(orm['semantic_blog.tag'], null=False))
        ))
        db.create_unique('semantic_blog_article_tags',
                         ['article_id', 'tag_id'])

        # Deleting field 'Enhancement.entity'
        db.delete_column('semantic_blog_enhancement', 'entity_id')

        # Adding field 'Enhancement.comment'
        db.add_column('semantic_blog_enhancement', 'comment',
                      self.gf('django.db.models.fields.CharField')(
                          max_length=20000, null=True), keep_default=False)


    def backwards(self, orm):
        # Adding model 'Entity'
        db.create_table('semantic_blog_entity', (
            ('comment',
             self.gf('django.db.models.fields.CharField')(max_length=20000)),
            ('id',
             self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('semantic_blog', ['Entity'])

        # Adding M2M table for field tags on 'Entity'
        db.create_table('semantic_blog_entity_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True,
                                    auto_created=True)),
            ('entity',
             models.ForeignKey(orm['semantic_blog.entity'], null=False)),
            ('tag', models.ForeignKey(orm['semantic_blog.tag'], null=False))
        ))
        db.create_unique('semantic_blog_entity_tags', ['entity_id', 'tag_id'])

        # Removing M2M table for field tags on 'Article'
        db.delete_table('semantic_blog_article_tags')

        # Adding field 'Enhancement.entity'
        db.add_column('semantic_blog_enhancement', 'entity',
                      self.gf('django.db.models.fields.related.ForeignKey')(
                          to=orm['semantic_blog.Entity'], null=True),
                      keep_default=False)

        # Deleting field 'Enhancement.comment'
        db.delete_column('semantic_blog_enhancement', 'comment')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': (
            'django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [],
                     {'unique': 'True', 'max_length': '80'}),
            'permissions': (
            'django.db.models.fields.related.ManyToManyField', [],
            {'to': "orm['auth.Permission']", 'symmetrical': 'False',
             'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {
            'ordering': "('content_type__app_label', 'content_type__model', "
                        "'codename')",
            'unique_together': "(('content_type', 'codename'),)",
            'object_name': 'Permission'},
            'codename': (
            'django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [],
                             {'to': "orm['contenttypes.ContentType']"}),
            'id': (
            'django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': (
            'django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [],
                            {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [],
                      {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [],
                           {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [],
                       {'to': "orm['auth.Group']", 'symmetrical': 'False',
                        'blank': 'True'}),
            'id': (
            'django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': (
            'django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': (
            'django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': (
            'django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [],
                           {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [],
                          {'max_length': '30', 'blank': 'True'}),
            'password': (
            'django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': (
            'django.db.models.fields.related.ManyToManyField', [],
            {'to': "orm['auth.Permission']", 'symmetrical': 'False',
             'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [],
                         {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)",
                     'unique_together': "(('app_label', 'model'),)",
                     'object_name': 'ContentType',
                     'db_table': "'django_content_type'"},
            'app_label': (
            'django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': (
            'django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': (
            'django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': (
            'django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'semantic_blog.article': {
            'Meta': {'object_name': 'Article'},
            'content': (
            'django.db.models.fields.CharField', [], {'max_length': '20000'}),
            'enhancements': (
            'django.db.models.fields.related.ManyToManyField', [],
            {'to': "orm['semantic_blog.Enhancement']",
             'symmetrical': 'False'}),
            'id': (
            'django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [],
                     {'to': "orm['semantic_blog.Tag']",
                      'symmetrical': 'False'}),
            'title': (
            'django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'semantic_blog.enhancement': {
            'Meta': {'object_name': 'Enhancement'},
            'comment': ('django.db.models.fields.CharField', [],
                        {'max_length': '20000', 'null': 'True'}),
            'id': (
            'django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': (
            'django.db.models.fields.CharField', [], {'max_length': '20000'})
        },
        'semantic_blog.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': (
            'django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [],
                    {'unique': 'True', 'max_length': '200'}),
            'value': (
            'django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'semantic_blog.userarticleconnection': {
            'Meta': {'object_name': 'UserArticleConnection'},
            'article': ('django.db.models.fields.related.ForeignKey', [],
                        {'to': "orm['semantic_blog.Article']"}),
            'connection': ('django.db.models.fields.IntegerField', [], {}),
            'id': (
            'django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [],
                     {'to': "orm['semantic_blog.UserProfile']"})
        },
        'semantic_blog.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'first_name': ('django.db.models.fields.CharField', [],
                           {'max_length': '50', 'blank': 'True'}),
            'id': (
            'django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [],
                          {'max_length': '50', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [],
                     {'to': "orm['auth.User']", 'unique': 'True',
                      'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['semantic_blog']
