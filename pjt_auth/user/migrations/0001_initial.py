# Generated by Django 3.0.8 on 2020-07-31 04:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category', models.CharField(max_length=45, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'category',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('idx', models.AutoField(primary_key=True, serialize=False)),
                ('channel_name', models.CharField(blank=True, max_length=100, null=True)),
                ('channel_url', models.CharField(max_length=200)),
                ('channel_description', models.CharField(blank=True, max_length=3000, null=True)),
                ('channel_start_date', models.DateField(blank=True, null=True)),
                ('need_process', models.BooleanField(blank=True, null=True)),
                ('channel_owner', models.CharField(blank=True, max_length=100, null=True)),
                ('temp', models.CharField(blank=True, max_length=10, null=True)),
                ('star_channel', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'db_table': 'channel',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ChannelCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'channel_category',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ChannelSubscriber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscriber_num', models.CharField(max_length=50)),
                ('check_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'channel_subscriber',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('idx', models.AutoField(primary_key=True, serialize=False)),
                ('comment_content', models.CharField(max_length=8000)),
                ('write_time', models.DateTimeField()),
                ('need_process', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'db_table': 'comment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('keyword', models.CharField(max_length=45, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'keyword',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('idx', models.AutoField(primary_key=True, serialize=False)),
                ('id', models.CharField(max_length=45)),
                ('phone', models.CharField(blank=True, max_length=45, null=True)),
                ('signup_date', models.DateField()),
                ('on_subscribe', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'db_table': 'user_info',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('idx', models.AutoField(primary_key=True, serialize=False)),
                ('video_name', models.CharField(max_length=500)),
                ('video_description', models.CharField(blank=True, max_length=5000, null=True)),
                ('video_url', models.CharField(max_length=100)),
                ('upload_time', models.DateTimeField()),
                ('need_process', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'db_table': 'video',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AnalysisChannel',
            fields=[
                ('channel_idx', models.OneToOneField(db_column='channel_idx', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='user.Channel')),
                ('insertion_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'analysis_channel',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CategoryAndKeyword',
            fields=[
                ('category', models.OneToOneField(db_column='category', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='user.Category')),
            ],
            options={
                'db_table': 'category_and_keyword',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CommentKeyword',
            fields=[
                ('comment_idx', models.OneToOneField(db_column='comment_idx', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='user.Comment')),
                ('keyword', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'comment_keyword',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CommentLikes',
            fields=[
                ('comment_idx', models.OneToOneField(db_column='comment_idx', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='user.Comment')),
                ('likes', models.CharField(max_length=50)),
                ('check_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'comment_likes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CommentSentiment',
            fields=[
                ('comment_idx', models.OneToOneField(db_column='comment_idx', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='user.Comment')),
                ('positive', models.FloatField(blank=True, null=True)),
                ('negative', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'comment_sentiment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='VideoKeyword',
            fields=[
                ('video_idx', models.OneToOneField(db_column='video_idx', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='user.Video')),
                ('keyword', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'video_keyword',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='VideoLikes',
            fields=[
                ('video_idx', models.OneToOneField(db_column='video_idx', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='user.Video')),
                ('likes', models.CharField(max_length=50)),
                ('check_time', models.DateTimeField()),
                ('dislikes', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'video_likes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='VideoViews',
            fields=[
                ('video_idx', models.OneToOneField(db_column='video_idx', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='user.Video')),
                ('views', models.IntegerField()),
                ('check_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'video_views',
                'managed': False,
            },
        ),
    ]