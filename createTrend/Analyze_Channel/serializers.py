from rest_framework import serializers
from .models import Channel,VideoKeywordNew, Video

class VideoKeywordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VideoKeywordNew
        fields = ['keyword']
        
class KeywordCountSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    value = serializers.IntegerField()