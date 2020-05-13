# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-05-05 03:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('respondant', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='survey.SurveyRespondant')),
                ('survey', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='survey.Survey')),
            ],
            options={
                'db_table': 'response',
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(max_length=100)),
                ('question', models.CharField(max_length=100)),
                ('totalchoice', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='question',
            name='respondant',
        ),
        migrations.RemoveField(
            model_name='question',
            name='survey',
        ),
        migrations.AddField(
            model_name='question',
            name='response',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='survey.Response'),
        ),
    ]