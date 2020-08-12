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
    class Meta:
        managed = False
        db_table = 'channel'
