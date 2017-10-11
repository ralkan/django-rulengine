# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('operator', models.CharField(max_length=255, choices=[(b'equal', b'Equal'), (b'not_equal', b'Not Equal'), (b'less', b'Less Than'), (b'greater', b'Greater Than'), (b'less_equal', b'Less Than or Equal'), (b'greater_equal', b'Greater Than or Equal'), (b'contains', b'String Contains'), (b'in', b'In')])),
                ('value', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContextValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('data_type', models.CharField(max_length=255, choices=[(b'str', b'String'), (b'int', b'Integer'), (b'float', b'Float'), (b'date', b'Date')])),
                ('implemented', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('operator', models.CharField(default=b'and', max_length=255, choices=[(b'and', b'And'), (b'or', b'Or')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RuleContext',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='rule',
            name='rule_context',
            field=models.ForeignKey(related_name='rules', to='djrulengine.RuleContext'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contextvalue',
            name='rule_context',
            field=models.ForeignKey(related_name='context_values', blank=True, to='djrulengine.RuleContext', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='condition',
            name='context_key',
            field=models.ForeignKey(related_name='conditions', to='djrulengine.ContextValue'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='condition',
            name='rule',
            field=models.ForeignKey(related_name='conditions', to='djrulengine.Rule'),
            preserve_default=True,
        ),
    ]
