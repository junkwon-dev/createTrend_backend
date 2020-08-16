# Generated by Django 3.0.8 on 2020-08-16 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Analyze_Channel', '0002_videoviews'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChannelSubscriber',
            fields=[
                ('subscriber_num', models.CharField(max_length=50)),
                ('check_time', models.DateTimeField()),
                ('idx', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'channel_subscriber',
                'managed': False,
            },
        ),
    ]
