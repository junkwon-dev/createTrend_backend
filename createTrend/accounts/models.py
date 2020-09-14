from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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



class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userinfo')
    phone = models.CharField(max_length=45, blank=True, null=True)
    on_subscribe = models.BooleanField(blank=True, null=True)
    own_channel = models.ForeignKey(Channel, models.DO_NOTHING, db_column='own_channel', blank=True, null=True)

    def set_phone(self, data):
        self.phone=data

    def set_on_subscribe(self,data):
        self.on_subscribe=data

    def set_own_channel(self,data):
        self.own_channel=data


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserInfo.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userinfo.save()