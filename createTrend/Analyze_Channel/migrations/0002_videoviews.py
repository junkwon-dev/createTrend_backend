# Generated by Django 3.0.8 on 2020-08-16 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Analyze_Channel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoViews',
            fields=[
                ('views', models.IntegerField()),
                ('check_time', models.DateTimeField()),
                ('idx', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'video_views',
                'managed': False,
            },
        ),
    ]
