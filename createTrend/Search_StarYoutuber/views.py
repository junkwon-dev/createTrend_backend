from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime, timedelta
from Search_StarYoutuber.serializers import ChannelInfoSerializer, ChannelSubscriberSerializer, ChannelListSerializer\
    , VideoSerializer,VideoViewsSerializer, VideoKeywordNewSerializer, KeywordCountSerializer\
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
        # topViewVideos=channel.video\
        #     .annotate(Max('videoviews__check_time'))\
        #     .order_by('-videoviews__views')[:5]
        videos = channel.video\
                .annotate(hottest_video_made_at=Max('videoviews__check_time')) 
        hottest_videos = VideoViews.objects.filter(
            check_time__in=[v.hottest_video_made_at for v in videos]
            ).order_by('-views')[:5]
        topViewVideos=[]
        for hv in hottest_videos:
            topViewVideos.append(hv.video_idx)
            
        topChannelSubscriber = channel.channelsubscriber\
            .order_by('-check_time')[:1]
            
        
        videos = channel.video.all().prefetch_related('videokeywordnew')
        keywords=[]
        
        for video in videos:
            keyword=[vk.keyword for vk in video.videokeywordnew.all()]
            keywords.append(keyword)
        keywords=list(itertools.chain(*keywords))
        counter=collections.Counter(keywords)
        keywords=dict(counter.most_common(n=10))
        keywords=[{"name":key,"value":keywords[key]} for key in keywords.keys()]
        class Keyword(object):
            def __init__(self,keyword):
                self.name = keyword['name']
                self.value=keyword['value']
        keywords=[Keyword(keyword=keyword) for keyword in keywords]
        start=timezone.now()-datetime.timedelta(days=50)
        start=start.strftime("%Y-%m-%d")
        end=timezone.now().strftime("%Y-%m-%d")    
        channelSubscribers=list(channel.channelsubscriber.filter(check_time__range=(start,end)).order_by('check_time'))
        ChannelSubscriber=[]
        for channelSubscirber in channelSubscribers:
            date=channelSubscirber.check_time
            value=channelSubscirber.subscriber_num
            date_value=str(date)[:10]
            ChannelSubscriber.append({"date":date_value,"value":value})
        keywordCountSerializer=KeywordCountSerializer(keywords,many=True)
        topChannelSubscriberSerializer=ChannelSubscriberSerializer(topChannelSubscriber,many=True)
        channelSerializer = ChannelInfoSerializer(channel)
        topViewVideoSerializer=VideoSerializer(topViewVideos,many=True)
        subscribernum=topChannelSubscriberSerializer.data[0]['subscriber_num']
        channelinfodict=channelSerializer.data
        channelinfodict['subscriber']=subscribernum
        # return Response({'ChannelInfo':channelSerializer.data, 'TopViewVideo':topViewVideoSerializer.data,'Keyword':videoKeywordSerializer.data})
        return Response({'channelInfo':channelinfodict, 'video':{"type":"aside","data":topViewVideoSerializer.data}\
            ,'keyword':{'pie':keywordCountSerializer.data},'line':{"type":"구독자수 추이","data":ChannelSubscriber}})
    
@api_view(['GET'])
def channelperioddata(request,pk):
    try:
        channel = Channel.objects\
            .get(pk=pk)
    except Channel.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        start=request.query_params.get('start')
        end=request.query_params.get('end')
        if(start and end):
            videos = channel.video.filter(upload_time__range=(start,end))\
                .annotate(hottest_video_made_at=Max('videoviews__check_time')) 
            
            hottest_videos = VideoViews.objects.filter(
                check_time__in=[v.hottest_video_made_at for v in videos]
                ).order_by('-views')[:5]
            topViewVideos=[]
            for hv in hottest_videos:
                topViewVideos.append(hv.video_idx)
            keywords=[]
            for video in videos:
                keyword=[vk.keyword for vk in video.videokeywordnew.all()]
                keywords.append(keyword)
            keywords=list(itertools.chain(*keywords))
            counter=collections.Counter(keywords)
            keywords=dict(counter.most_common(n=10))
            keywords=[{"name":key,"value":keywords[key]} for key in keywords.keys()]
            class Keyword(object):
                def __init__(self,keyword):
                    self.name = keyword['name']
                    self.value=keyword['value']
            keywords=[Keyword(keyword=keyword) for keyword in keywords]


            keywordCountSerializer=KeywordCountSerializer(keywords,many=True)
            videoSerializer=VideoSerializer(topViewVideos,many=True)
            return Response({'video':{"type":"analysis","data":videoSerializer.data}, 'keyword':{"pie":keywordCountSerializer.data}})
        else:
            start=timezone.now()-datetime.timedelta(days=14)
            start=start.strftime("%Y-%m-%d")
            end=timezone.now().strftime("%Y-%m-%d")    
            channelSubscriber=channel.channelsubscriber.filter(check_time__range=(start,end))
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
      

    