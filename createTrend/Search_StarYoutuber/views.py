from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from Search_StarYoutuber.serializers import ChannelInfoSerializer, ChannelSubscriberSerializer, ChannelListSerializer\
    , VideoSerializer,VideoViewsSerializer, VideoKeywordSerializer, KeywordCountSerializer\
    , ChannelViewsCountSerializer
from rest_framework.pagination import PageNumberPagination
from .models import Channel, ChannelSubscriber, VideoViews,Video
from itertools import chain
from django.db.models import Max 
import collections, itertools, datetime
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
            
        
        videos = channel.video.all().prefetch_related('videokeyword')
        keywords=[]
        
        for video in videos:
            keyword=[videokeyword.keyword for videokeyword in video.videokeyword.all()]
            keywords.append(keyword)
        keywords=list(itertools.chain(*keywords))
        counter=collections.Counter(keywords)
        keywords=dict(counter.most_common(n=10))
        class Keyword(object):
            def __init__(self,keyword):
                self.keyword = keyword
        keywords=Keyword(keyword=keywords)
        
        
        keywordCountSerializer=KeywordCountSerializer(keywords)
        topChannelSubscriberSerializer=ChannelSubscriberSerializer(topChannelSubscriber,many=True)
        channelSerializer = ChannelInfoSerializer(channel)
        topViewVideoSerializer=VideoSerializer(topViewVideos,many=True)
        # return Response({'ChannelInfo':channelSerializer.data, 'TopViewVideo':topViewVideoSerializer.data,'Keyword':videoKeywordSerializer.data})
        return Response({'ChannelInfo':channelSerializer.data, 'TopViewVideo':topViewVideoSerializer.data\
            ,'TopChannelSubscirber':topChannelSubscriberSerializer.data,'KeywordCount':keywordCountSerializer.data})
    
@api_view(['GET'])
def channelviewscount(request,pk):
    try:
        channel = Channel.objects\
            .get(pk=pk)
    except Channel.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        start=request.query_params.get('start')
        end=request.query_params.get('end')
        if(start and end):
            channelviews=channel.channelsubscriber.filter(check_time__range=(start,end))
            videos=channel.video.filter(upload_time__range=(start,end))
            videos = channel.video.filter(upload_time__range=(start,end)).prefetch_related('videokeyword')
            keywords=[]

            for video in videos:
                keyword=[videokeyword.keyword for videokeyword in video.videokeyword.all()]
                keywords.append(keyword)
            keywords=list(itertools.chain(*keywords))
            counter=collections.Counter(keywords)
            keywords=dict(counter.most_common(n=10))
            class Keyword(object):
                def __init__(self,keyword):
                    self.keyword = keyword
            keywords=Keyword(keyword=keywords)


            keywordCountSerializer=KeywordCountSerializer(keywords)
            videoSerializer=VideoSerializer(videos,many=True)
            channelSubscriberSerializer=ChannelSubscriberSerializer(channelviews,many=True)
            return Response({'ChannelSubscriber':channelSubscriberSerializer.data,'Video':videoSerializer.data, 'Keyword':keywordCountSerializer.data})
        else:    
            channelSubscriber=channel.channelsubscriber.all()
            channelSubscriberSerializer=ChannelSubscriberSerializer(channelSubscriber,many=True)
            return Response(channelSubscriberSerializer.data)

@api_view(['GET'])
def channellist(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10
    queryset = Channel.objects.all()
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = ChannelListSerializer(result_page,many=True)
    return paginator.get_paginated_response(serializer.data) 
      

    