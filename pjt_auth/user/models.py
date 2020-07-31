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
    channel_url = models.CharField(max_length=200)
    channel_description = models.CharField(max_length=3000, blank=True, null=True)
    channel_start_date = models.DateField(blank=True, null=True)
    need_process = models.BooleanField(blank=True, null=True)
    channel_owner = models.CharField(max_length=100, blank=True, null=True)
    temp = models.CharField(max_length=10, blank=True, null=True)
    star_channel = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'channel'


class ChannelCategory(models.Model):
    channel_idx = models.ForeignKey(Channel, models.DO_NOTHING, db_column='channel_idx', blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING, db_column='category', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'channel_category'


class ChannelSubscriber(models.Model):
    channel_idx = models.ForeignKey(Channel, models.DO_NOTHING, db_column='channel_idx')
    subscriber_num = models.CharField(max_length=50)
    check_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'channel_subscriber'


class Comment(models.Model):
    idx = models.AutoField(primary_key=True)
    video_idx = models.ForeignKey('Video', models.DO_NOTHING, db_column='video_idx', blank=True, null=True)
    comment_content = models.CharField(max_length=8000)
    write_time = models.DateTimeField()
    need_process = models.BooleanField(blank=True, null=True)

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
    comment_idx = models.OneToOneField(Comment, models.DO_NOTHING, db_column='comment_idx', primary_key=True)
    likes = models.CharField(max_length=50)
    check_time = models.DateTimeField(blank=True, null=True)

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


class Keyword(models.Model):
    keyword = models.CharField(primary_key=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'keyword'


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
    video_url = models.CharField(max_length=100)
    upload_time = models.DateTimeField()
    channel_idx = models.ForeignKey(Channel, models.DO_NOTHING, db_column='channel_idx', blank=True, null=True)
    need_process = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'video'


class VideoKeyword(models.Model):
    video_idx = models.OneToOneField(Video, models.DO_NOTHING, db_column='video_idx', primary_key=True)
    keyword = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'video_keyword'


class VideoLikes(models.Model):
    video_idx = models.OneToOneField(Video, models.DO_NOTHING, db_column='video_idx', primary_key=True)
    likes = models.CharField(max_length=50)
    check_time = models.DateTimeField()
    dislikes = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'video_likes'


class VideoViews(models.Model):
    video_idx = models.OneToOneField(Video, models.DO_NOTHING, db_column='video_idx', primary_key=True)
    views = models.IntegerField()
    check_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'video_views'
