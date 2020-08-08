# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AnalysisChannel(models.Model):
    channel_idx = models.OneToOneField('Channel', models.DO_NOTHING, db_column='channel_idx', primary_key=True)
    insertion_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'analysis_channel'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Category(models.Model):
    category = models.CharField(primary_key=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'category'


class CategoryAndKeyword(models.Model):
    category = models.OneToOneField(Category, models.DO_NOTHING, db_column='category', primary_key=True)
    keyword = models.ForeignKey('Keyword', models.DO_NOTHING, db_column='keyword', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category_and_keyword'


class Channel(models.Model):
    idx = models.AutoField(primary_key=True)
    channel_name = models.CharField(max_length=100, blank=True, null=True)
    channel_id = models.CharField(max_length=200)
    channel_description = models.CharField(max_length=3000, blank=True, null=True)
    channel_start_date = models.DateField(blank=True, null=True)
    processed = models.BooleanField(blank=True, null=True)
    upload_id = models.CharField(max_length=1000, blank=True, null=True)
    hidden_subscriber = models.BooleanField(blank=True, null=True)
    topic_ids = models.CharField(max_length=2000, blank=True, null=True)
    topic_categories = models.CharField(max_length=5000, blank=True, null=True)
    thumbnail_url = models.CharField(max_length=200, blank=True, null=True)
    temp = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'channel'


class ChannelCategory(models.Model):
    channel_idx = models.ForeignKey(Channel, models.DO_NOTHING, db_column='channel_idx', blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING, db_column='category', blank=True, null=True)
    idx = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'channel_category'


class ChannelSubscriber(models.Model):
    channel_idx = models.ForeignKey(Channel, models.DO_NOTHING, db_column='channel_idx')
    subscriber_num = models.CharField(max_length=50)
    check_time = models.DateTimeField()
    idx = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'channel_subscriber'


class Comment(models.Model):
    idx = models.AutoField(primary_key=True)
    video_idx = models.ForeignKey('Video', models.DO_NOTHING, db_column='video_idx', blank=True, null=True)
    comment_content = models.CharField(max_length=8000)
    write_time = models.DateTimeField()
    processed = models.BooleanField(blank=True, null=True)
    writer_name = models.CharField(max_length=200, blank=True, null=True)
    writer_img_url = models.CharField(max_length=200, blank=True, null=True)
    comment_id = models.CharField(unique=True, max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comment'


class CommentKeyword(models.Model):
    comment_idx = models.OneToOneField(Comment, models.DO_NOTHING, db_column='comment_idx', primary_key=True)
    keyword = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'comment_keyword'


class CommentLikes(models.Model):
    comment_idx = models.ForeignKey(Comment, models.DO_NOTHING, db_column='comment_idx')
    likes = models.IntegerField()
    check_time = models.DateTimeField(blank=True, null=True)
    idx = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'comment_likes'


class CommentSentiment(models.Model):
    comment_idx = models.OneToOneField(Comment, models.DO_NOTHING, db_column='comment_idx', primary_key=True)
    positive = models.FloatField(blank=True, null=True)
    negative = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comment_sentiment'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Keyword(models.Model):
    keyword = models.CharField(primary_key=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'keyword'


class ThumbnailLogo(models.Model):
    idx = models.AutoField(primary_key=True)
    video_idx = models.ForeignKey('Video', models.DO_NOTHING, db_column='video_idx', blank=True, null=True)
    logo = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'thumbnail_logo'


class ThumbnailObjects(models.Model):
    idx = models.AutoField(primary_key=True)
    video_idx = models.ForeignKey('Video', models.DO_NOTHING, db_column='video_idx', blank=True, null=True)
    object = models.CharField(max_length=200, blank=True, null=True)
    object_score = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'thumbnail_objects'


class UserInfo(models.Model):
    idx = models.AutoField(primary_key=True)
    id = models.CharField(max_length=45)
    phone = models.CharField(max_length=45, blank=True, null=True)
    signup_date = models.DateField()
    on_subscribe = models.BooleanField(blank=True, null=True)
    own_channel = models.ForeignKey(Channel, models.DO_NOTHING, db_column='own_channel', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_info'


class Video(models.Model):
    idx = models.AutoField(primary_key=True)
    video_name = models.CharField(max_length=500)
    video_description = models.CharField(max_length=5000, blank=True, null=True)
    video_id = models.CharField(unique=True, max_length=100)
    upload_time = models.DateTimeField()
    channel_idx = models.ForeignKey(Channel, models.DO_NOTHING, db_column='channel_idx', blank=True, null=True)
    processed = models.BooleanField(blank=True, null=True)
    thumbnail_url = models.CharField(max_length=200, blank=True, null=True)
    thumbnail_processed = models.BooleanField(blank=True, null=True)
    forbidden = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'video'


class VideoKeyword(models.Model):
    video_idx = models.ForeignKey(Video, models.DO_NOTHING, db_column='video_idx')
    keyword = models.CharField(max_length=100)
    idx = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'video_keyword'
        unique_together = (('video_idx', 'keyword'),)


class VideoLikes(models.Model):
    video_idx = models.ForeignKey(Video, models.DO_NOTHING, db_column='video_idx')
    likes = models.IntegerField()
    check_time = models.DateTimeField()
    dislikes = models.IntegerField(blank=True, null=True)
    idx = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'video_likes'


class VideoViews(models.Model):
    video_idx = models.ForeignKey(Video, models.DO_NOTHING, db_column='video_idx')
    views = models.IntegerField()
    check_time = models.DateTimeField()
    idx = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'video_views'
