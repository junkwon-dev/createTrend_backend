from rest_framework import serializers
from .models import Channel, ChannelSubscriber

# 사용자 목록
        
class SubscriberNumberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChannelSubscriber
        fields = ['subscriber_num','check_time']

class ChannelInfoSerializer(serializers.HyperlinkedModelSerializer):  
    channel_subscriber=SubscriberNumberSerializer(many=True, read_only = True)
    class Meta:
        model = Channel
        fields = ('thumbnail_url', 'channel_description', 'channel_name', 'channel_start_date','channel_subscriber')