from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from Search_StarYoutuber.serializers import ChannelInfoSerializer, SubscriberNumberSerializer
from rest_framework.pagination import PageNumberPagination
from .models import Channel, ChannelSubscriber
from itertools import chain
# Create your views here.

@api_view(['GET'])
def channelinfo(request,pk):
    try:
        channel = Channel.objects.get(pk=pk)
    except Channel.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ChannelInfoSerializer(channel)
        return Response(serializer.data)
    
@api_view(['GET'])
def channellist(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10
    queryset = Channel.objects.prefetch_related('channelsubscriber').all()
    print(queryset)
    # queryset = Channel.channelsubscriber.objects.all()
    channels=[]
    # query2=channel.channelsubscriber.filter(channel_idx=channel.idx).all()
    for channel in queryset:
        subscriber_num = [{'subscriber_num':channel_subscriber.subscriber_num,'check_time':channel_subscriber.check_time} for channel_subscriber in channel.channelsubscriber.filter(channel_idx=channel.idx).all()]
        # print(subscriber_num)
        channels.append({'thumbnail_url':channel.thumbnail_url, 'channel_description':channel.channel_description, 'channel_name':channel.channel_name, 'channel_start_date':channel.channel_start_date,'channel_subscriber':subscriber_num})

    result_page = paginator.paginate_queryset(channels, request)
    serializer = ChannelInfoSerializer(result_page,many=True)
    return paginator.get_paginated_response(serializer.data)
      

    