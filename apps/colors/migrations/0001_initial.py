# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.colors.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, db_index=True)),
                ('hex', models.CharField(max_length=255, db_index=True)),
                ('r', models.IntegerField()),
                ('g', models.IntegerField()),
                ('b', models.IntegerField()),
                ('priority', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='ImageFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('basename', models.CharField(max_length=255, db_index=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('source', apps.colors.fields.ContentTypeRestrictedImageField(upload_to=b'images/')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='color',
            name='image',
            field=models.ForeignKey(related_query_name=b'color', related_name='colors', to='colors.ImageFile'),
        ),
    ]
