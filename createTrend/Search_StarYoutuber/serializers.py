from rest_framework import serializers
from .models import Channel, ChannelSubscriber, VideoViews, Video

# 사용자 목록
        
class SubscriberNumberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChannelSubscriber
        fields = ['check_time','subscriber_num']

class ChannelListSerializer(serializers.HyperlinkedModelSerializer):  
    channelsubscriber=SubscriberNumberSerializer(many=True, read_only = True)
    class Meta:
        model = Channel
        fields = ['thumbnail_url', 'channel_description', 'channel_name', 'channel_start_date','channelsubscriber']

class VideoViewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VideoViews
        fields = ['check_time','views']

class VideoSerializer(serializers.HyperlinkedModelSerializer):
    videoviews=VideoViewsSerializer(many=True,read_only=True)
    class Meta:
        model = Video
        fields = ['video_name','video_description','video_id','upload_time','processed','thumbnail_url','thumbnail_processed','videoviews']

class ChannelInfoSerializer(serializers.HyperlinkedModelSerializer):
    channelsubscriber=SubscriberNumberSerializer(many=True, read_only = True)
    videoviews=VideoViewsSerializer(many=True,read_only=True)
    class Meta:
        model = Channel
        fields = ['thumbnail_url', 'channel_description', 'channel_name', 'channel_start_date','channelsubscriber','videoviews']
        
