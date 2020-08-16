from rest_framework import serializers
from .models import Channel, ChannelSubscriber, VideoViews, Video, VideoKeywordNew,ChannelViews

# 사용자 목록
        
class ChannelSubscriberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChannelSubscriber
        fields = ['check_time','subscriber_num']

class ChannelListSerializer(serializers.HyperlinkedModelSerializer):  
    # channelsubscriber=SubscriberNumberSerializer(many=True, read_only = True)
    class Meta:
        model = Channel
        fields = ['thumbnail_url', 'channel_description', 'channel_name', 'channel_start_date']

class ChannelViewsCountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChannelViews
        fields = ['view_count','check_time']

class VideoKeywordNewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VideoKeywordNew
        fields = ['keyword']

class VideoViewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VideoViews
        fields = ['check_time','views']

class VideoSerializer(serializers.HyperlinkedModelSerializer):
    videoviews=VideoViewsSerializer(many=True,read_only=True)
    videokeywordnew=VideoKeywordNewSerializer(many=True,read_only=True)
    class Meta:
        model = Video
        fields = ['video_name','video_description','video_id','upload_time','processed','thumbnail_url','thumbnail_processed','videoviews','videokeywordnew']

class ChannelInfoSerializer(serializers.HyperlinkedModelSerializer):
    videoviews=VideoViewsSerializer(many=True,read_only=True)
    class Meta:
        model = Channel
        fields = ['idx','thumbnail_url', 'channel_description', 'channel_name', 'channel_start_date','videoviews']
        
class KeywordCountSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    value = serializers.IntegerField()