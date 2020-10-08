from rest_framework import serializers
from .models import Channel, VideoViews, Video


class VideoViewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VideoViews
        fields = ['check_time','views']



class VideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Video
        fields = ['video_name','video_id','thumbnail_url']
        
class ChannelSerializer(serializers.HyperlinkedModelSerializer):  
    # channelsubscriber=SubscriberNumberSerializer(many=True, read_only = True)
    class Meta:
        model = Channel
        fields = ['thumbnail_url', 'channel_description', 'channel_name', 'subscriber_num']