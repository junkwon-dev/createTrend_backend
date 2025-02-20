# Generated by Django 3.0.8 on 2020-08-10 07:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.BooleanField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.BooleanField()),
                ('is_active', models.BooleanField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
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
                ('channel_id', models.CharField(max_length=200)),
                ('channel_description', models.CharField(blank=True, max_length=3000, null=True)),
                ('channel_start_date', models.DateField(blank=True, null=True)),
                ('processed', models.BooleanField(blank=True, null=True)),
                ('upload_id', models.CharField(blank=True, max_length=1000, null=True)),
                ('hidden_subscriber', models.BooleanField(blank=True, null=True)),
                ('thumbnail_url', models.CharField(blank=True, max_length=200, null=True)),
                ('temp', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'db_table': 'channel',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ChannelCategory',
            fields=[
                ('idx', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'channel_category',
                'managed': False,
            },
        ),
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
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('idx', models.AutoField(primary_key=True, serialize=False)),
                ('comment_content', models.CharField(max_length=8000)),
                ('write_time', models.DateTimeField()),
                ('processed', models.BooleanField(blank=True, null=True)),
                ('writer_name', models.CharField(blank=True, max_length=200, null=True)),
                ('writer_img_url', models.CharField(blank=True, max_length=200, null=True)),
                ('comment_id', models.CharField(blank=True, max_length=100, null=True, unique=True)),
            ],
            options={
                'db_table': 'comment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CommentLikes',
            fields=[
                ('likes', models.IntegerField()),
                ('check_time', models.DateTimeField(blank=True, null=True)),
                ('idx', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'comment_likes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.SmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
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
            name='ThumbnailLogo',
            fields=[
                ('idx', models.AutoField(primary_key=True, serialize=False)),
                ('logo', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'thumbnail_logo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ThumbnailObjects',
            fields=[
                ('idx', models.AutoField(primary_key=True, serialize=False)),
                ('object', models.CharField(blank=True, max_length=200, null=True)),
                ('object_score', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'thumbnail_objects',
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
                ('video_id', models.CharField(max_length=100, unique=True)),
                ('upload_time', models.DateTimeField()),
                ('processed', models.BooleanField(blank=True, null=True)),
                ('thumbnail_url', models.CharField(blank=True, max_length=200, null=True)),
                ('thumbnail_processed', models.BooleanField(blank=True, null=True)),
                ('forbidden', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'db_table': 'video',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='VideoKeyword',
            fields=[
                ('keyword', models.CharField(max_length=100)),
                ('idx', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'video_keyword',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='VideoLikes',
            fields=[
                ('likes', models.IntegerField()),
                ('check_time', models.DateTimeField()),
                ('dislikes', models.IntegerField(blank=True, null=True)),
                ('idx', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'video_likes',
                'managed': False,
            },
        ),
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
        migrations.CreateModel(
            name='AnalysisChannel',
            fields=[
                ('channel_idx', models.OneToOneField(db_column='channel_idx', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='Search_StarYoutuber.Channel')),
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
                ('category', models.OneToOneField(db_column='category', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='Search_StarYoutuber.Category')),
            ],
            options={
                'db_table': 'category_and_keyword',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CommentKeyword',
            fields=[
                ('comment_idx', models.OneToOneField(db_column='comment_idx', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='Search_StarYoutuber.Comment')),
                ('keyword', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'comment_keyword',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CommentSentiment',
            fields=[
                ('comment_idx', models.OneToOneField(db_column='comment_idx', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='Search_StarYoutuber.Comment')),
                ('positive', models.FloatField(blank=True, null=True)),
                ('negative', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'comment_sentiment',
                'managed': False,
            },
        ),
    ]
