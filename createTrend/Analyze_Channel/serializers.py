from rest_framework import serializers
from .models import Channel,VideoKeywordNew, Video


class VideoKeywordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VideoKeywordNew
        fields = ['keyword']


class VideoSerializer(serializers.HyperlinkedModelSerializer):
    videokeywordnew=VideoKeywordSerializer(many=True,read_only=True)
    class Meta:
        model = Video
        fields = ['idx','video_name','video_id','thumbnail_url','videokeywordnew','popularity','views']


class TopVideoSerializer(serializers.HyperlinkedModelSerializer):
    # videokeywordnew=VideoKeywordSerializer(many=True,read_only=True)
    class Meta:
        model = Video
        fields = ['idx','video_name','views','views_growth']

        
class KeywordCountSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    value = serializers.IntegerField()