from rest_framework import serializers
from .models import Channel,VideoKeywordNew, VideoViews, Video

class ChannelListSerializer(serializers.HyperlinkedModelSerializer):  
    # channelsubscriber=SubscriberNumberSerializer(many=True, read_only = True)
    class Meta:
        model = Channel
        fields = ['thumbnail_url', 'channel_description', 'channel_name', 'channel_start_date']

class VideoViewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VideoViews
        fields = ['check_time','views']

class VideoKeywordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VideoKeywordNew
        fields = ['keyword']
        
class TopVideoSerializer(serializers.HyperlinkedModelSerializer):
    # videoviews=VideoViewsSerializer(many=True,read_only=True)
    videokeywordnew=VideoKeywordSerializer(many=True,read_only=True)
    class Meta:
        model = Video
        fields = ['idx','video_name','video_id','thumbnail_url','videokeywordnew','popularity','views']

class RecentVideoSerializer(serializers.HyperlinkedModelSerializer):
    # videoviews=VideoViewsSerializer(many=True,read_only=True)
    videokeywordnew=VideoKeywordSerializer(many=True,read_only=True)
    class Meta:
        model = Video
        fields = ['idx','video_name','video_id','thumbnail_url','popularity','views','views_growth','videokeywordnew']
        
class KeywordCountSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    value = serializers.IntegerField()