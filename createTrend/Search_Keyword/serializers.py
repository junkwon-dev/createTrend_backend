from rest_framework import serializers
from .models import Channel

class ChannelListSerializer(serializers.HyperlinkedModelSerializer):  
    # channelsubscriber=SubscriberNumberSerializer(many=True, read_only = True)
    class Meta:
        model = Channel
        fields = ['thumbnail_url', 'channel_description', 'channel_name', 'channel_start_date']
