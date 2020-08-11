from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from Search_StarYoutuber.serializers import ChannelInfoSerializer, SubscriberNumberSerializer, ChannelListSerializer\
    , VideoSerializer,VideoViewsSerializer, VideoKeywordSerializer, SubscriberNumberSerializer
from rest_framework.pagination import PageNumberPagination
from .models import Channel, ChannelSubscriber, VideoViews,Video
from itertools import chain
from django.db.models import Max 
# Create your views here.

@api_view(['GET'])
def channelinfo(request,pk):
    try:
        channel = Channel.objects\
            .get(pk=pk)
    except Channel.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        topViewVideos=channel.video\
            .annotate(Max('videoviews__check_time'))\
            .order_by('-videoviews__views')[:5]
        topChannelSubscriber = channel.channelsubscriber\
            .order_by('-check_time')[:5]
        # videos = channel.video.all()[:5]
        # videokeywords=[]
        # for video in videos:
        #     keywords = [keywordquery.keyword for keywordquery in video.videokeyword.all()]
        #     videokeywords.append(keywords)
        
        # videoKeywordSerializer=VideoKeywordSerializer(keywords,many=True)
        topChannelSubscriberSerializer=SubscriberNumberSerializer(topChannelSubscriber,many=True)
        channelSerializer = ChannelInfoSerializer(channel)
        topViewVideoSerializer=VideoSerializer(topViewVideos,many=True)
        # return Response({'ChannelInfo':channelSerializer.data, 'TopViewVideo':topViewVideoSerializer.data,'Keyword':videoKeywordSerializer.data})
        return Response({'ChannelInfo':channelSerializer.data, 'TopViewVideo':topViewVideoSerializer.data\
            ,'TopChannelSubscirber':topChannelSubscriberSerializer.data})
    
@api_view(['GET'])
def channellist(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10
    queryset = Channel.objects.all()
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = ChannelListSerializer(result_page,many=True)
    return paginator.get_paginated_response(serializer.data) 
      

    