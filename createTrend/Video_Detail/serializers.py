from rest_framework import serializers
from .models import Channel, VideoViews, Video,VideoLikes,VideoKeywordNew


class VideoViewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VideoViews
        fields = ['check_time','views']

class VideoKeywordNewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VideoKeywordNew
        fields = ['keyword']

class VideoLikesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VideoLikes
        fields = ['likes','dislikes']
        
class VideoSerializer(serializers.HyperlinkedModelSerializer):
    videolikes=VideoLikesSerializer(many=True,read_only=True)
    videokeywordnew=VideoKeywordNewSerializer(many=True,read_only=True)
    class Meta:
        model = Video
        fields = ['video_name','video_id','thumbnail_url','video_description','videolikes','videokeywordnew']
        
class ChannelSerializer(serializers.HyperlinkedModelSerializer):  
    # channelsubscriber=SubscriberNumberSerializer(many=True, read_only = True)
    class Meta:
        model = Channel
        fields = ['thumbnail_url', 'channel_description', 'channel_name', 'subscriber_num']
        



