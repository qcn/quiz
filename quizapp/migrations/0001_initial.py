# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-04 10:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MCAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500)),
                ('short_text', models.CharField(max_length=30)),
                ('correct', models.BooleanField()),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='MCQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=1000)),
                ('randomise_answers', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SAQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=1000)),
                ('qz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizapp.Quiz')),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='mcquestion',
            name='qz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizapp.Quiz'),
        ),
        migrations.AddField(
            model_name='mcanswer',
            name='qn',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizapp.MCQuestion'),
        ),
    ]
