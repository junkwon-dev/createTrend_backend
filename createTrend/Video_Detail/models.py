from django.db import models

# Create your models here.
class Channel(models.Model):
    idx = models.AutoField(primary_key=True)
    channel_name = models.CharField(max_length=100, blank=True, null=True)
    channel_id = models.CharField(max_length=200)
    channel_description = models.CharField(max_length=3000, blank=True, null=True)
    channel_start_date = models.DateField(blank=True, null=True)
    processed = models.BooleanField(blank=True, null=True)
    upload_id = models.CharField(max_length=1000, blank=True, null=True)
    hidden_subscriber = models.BooleanField(blank=True, null=True)
    thumbnail_url = models.CharField(max_length=200, blank=True, null=True)
    temp = models.CharField(max_length=100, blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)
    subscriber_num=models.IntegerField()
    class Meta:
        managed = False
        db_table = 'channel'
class Video(models.Model):
    idx = models.AutoField(primary_key=True)
    video_name = models.CharField(max_length=500)
    video_description = models.CharField(max_length=5000, blank=True, null=True)
    video_id = models.CharField(unique=True, max_length=100)
    upload_time = models.DateTimeField()
    popularity= models.FloatField()
    views = models.IntegerField()
    channel_idx = models.ForeignKey(Channel, models.DO_NOTHING, db_column='channel_idx', blank=True, null=True,related_name='video')
    processed = models.BooleanField(blank=True, null=True)
    thumbnail_url = models.CharField(max_length=200, blank=True, null=True)
    thumbnail_processed = models.BooleanField(blank=True, null=True)
    forbidden = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'video'

class VideoViews(models.Model):
    video_idx = models.ForeignKey(Video, models.DO_NOTHING, db_column='video_idx', related_name='videoviews')
    views = models.IntegerField()
    check_time = models.DateTimeField()
    idx = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'video_views'

class VideoLikes(models.Model):
    video_idx = models.ForeignKey(Video, models.DO_NOTHING, db_column='video_idx', related_name='videolikes')
    likes = models.IntegerField()
    check_time = models.DateTimeField()
    dislikes = models.IntegerField(blank=True, null=True)
    idx = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'video_likes'
        
class VideoKeywordNew(models.Model):
    video_idx = models.ForeignKey(Video, models.DO_NOTHING, db_column='video_idx', related_name='videokeywordnew')
    keyword = models.CharField(max_length=100)
    idx = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'video_keyword_new'
        unique_together = (('video_idx', 'keyword'),)
