from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from Search_StarYoutuber.serializers import ChannelInfoSerializer, SubscriberNumberSerializer, ChannelListSerializer, VideoSerializer,VideoViewsSerializer
from rest_framework.pagination import PageNumberPagination
from .models import Channel, ChannelSubscriber, VideoViews,Video
from itertools import chain
from django.db.models import Max 
# Create your views here.

@api_view(['GET'])
def channelinfo(request,pk):
    try:
        channel = Channel.objects.get(pk=pk)
    except Channel.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        videos=channel.video\
            .annotate(Max('videoviews__check_time'))\
            .order_by('-videoviews__views')[:5]
        channelSerializer = ChannelInfoSerializer(channel)
        videoSerializer=VideoSerializer(videos,many=True)
        return Response({'ChannelInfo':channelSerializer.data, 'TopViewVideo':videoSerializer.data})
    
@api_view(['GET'])
def channellist(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10
    queryset = Channel.objects.all()
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = ChannelListSerializer(result_page,many=True)
    return paginator.get_paginated_response(serializer.data) 
      

    