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
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import collections, itertools, datetime

# Create your views here.

@api_view(['GET'])
def channelinfo(request,pk):
    '''
    채널 정보 API
    ---
    해당되는 채널의 정보, 채널을 분석해서 제공하는 API입니다.
    '''
    try:
        channel = Channel.objects\
            .get(pk=pk)
    except Channel.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
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


        videos = channel.video.prefetch_related('videokeywordnew')
        keywords=[]
        
        for video in videos:
            keyword=[vk.keyword for vk in video.videokeywordnew.all()]
            keywords.append(keyword)

        channel_name = channel.channel_name
        keywords=list(itertools.chain(*keywords))
        while channel_name in keywords:
            keywords.remove(channel_name)
        counter=collections.Counter(keywords)
        keywords=dict(counter.most_common(n=7))


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
        wordmapItems = keywordCountSerializer.data
        for itemIndex in range(len(wordmapItems)):
            if itemIndex == 0:
                wordmapItems[itemIndex].update({'color': '#f9bf69'})
            elif itemIndex == 1:
                wordmapItems[itemIndex].update({'color': '#f65a5a'})
            elif itemIndex == 2:
                wordmapItems[itemIndex].update({'color': '#508ddc'})
            elif itemIndex == 3:
                wordmapItems[itemIndex].update({'color': '#f9bf69'})
            elif itemIndex == 4:
                wordmapItems[itemIndex].update({'color': '#f65a5a'})
            else:
                wordmapItems[itemIndex].update({'color': '#508ddc'})
        return Response({'channelInfo':channelinfodict, 'video':{"type":"aside","data":topViewVideoSerializer.data}\
            , 'keyword':{'pie':keywordCountSerializer.data},'wordmap': {'name': channel_name, 'color': '#666', 'children': wordmapItems},'line':{"type":"구독자수 추이","data":ChannelSubscriber}})
    
param_channelperioddata_start_hint = openapi.Parameter(
        'start',
        openapi.IN_QUERY,
        description='기간 내의 영상을 검색합니다. 시작 날짜를 YYYY-mm-dd형태로 입력하세요.',
        type=openapi.TYPE_STRING
    )
param_channelperioddata_end_hint = openapi.Parameter(
        'end',
        openapi.IN_QUERY,
        description='기간 내의 영상을 검색합니다. 마지막 날짜를 YYYY-mm-dd형태로 입력하세요.',
        type=openapi.TYPE_STRING
)

@swagger_auto_schema(method='get',manual_parameters=[param_channelperioddata_start_hint,param_channelperioddata_end_hint])
@api_view(['GET'])
def channelperioddata(request,pk):
    '''
    채널의 기간 내 DATA API
    ---
    해당 채널에서 기간을 설정하면 그 기간 내 인기 영상, 구독자 수 추이 등을 제공하는 API입니다.
    '''
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
            channel_name=channel.channel_name
            while channel_name in keywords:
                keywords.remove(channel_name)
            counter=collections.Counter(keywords)
            keywords=dict(counter.most_common(n=7))
            keywords=[{"name":key,"value":keywords[key]} for key in keywords.keys()]
            class Keyword(object):
                def __init__(self,keyword):
                    self.name = keyword['name']
                    self.value=keyword['value']
            keywords=[Keyword(keyword=keyword) for keyword in keywords]


            keywordCountSerializer=KeywordCountSerializer(keywords,many=True)
            videoSerializer=VideoSerializer(topViewVideos,many=True)
            wordmapItems = keywordCountSerializer.data
            for itemIndex in range(len(wordmapItems)):
                if itemIndex == 0:
                    wordmapItems[itemIndex].update({'color': '#f9bf69'})
                elif itemIndex == 1:
                    wordmapItems[itemIndex].update({'color': '#f65a5a'})
                elif itemIndex == 2:
                    wordmapItems[itemIndex].update({'color': '#508ddc'})
                elif itemIndex == 3:
                    wordmapItems[itemIndex].update({'color': '#f9bf69'})
                elif itemIndex == 4:
                    wordmapItems[itemIndex].update({'color': '#f65a5a'})
                else:
                    wordmapItems[itemIndex].update({'color': '#508ddc'})
            return Response({'video':{"type":"analysis","data":videoSerializer.data},'keyword':{'pie':keywordCountSerializer.data}, 'wordmap': {'name': channel_name, 'color': '#666', 'children': wordmapItems}})
        else:
            start=timezone.now()-datetime.timedelta(days=14)
            start=start.strftime("%Y-%m-%d")
            end=timezone.now().strftime("%Y-%m-%d")    
            channelSubscriber=channel.channelsubscriber.filter(check_time__range=(start,end))
            channelSubscriberSerializer=ChannelSubscriberSerializer(channelSubscriber,many=True)
            return Response(channelSubscriberSerializer.data)

@api_view(['GET'])
def channellist(request): 
    '''
    채널리스트 API
    ---
    전체 채널의 목록을 보여주는 API입니다.
    '''
    youtuber_name = request.query_params.get('youtuber_name')

    if youtuber_name is not None:
        paginator = PageNumberPagination()
        paginator.page_size = 10
        channel_querysets = list(Channel.objects.prefetch_related('video','channelviews').filter(channel_name__icontains=youtuber_name).order_by('-subscriber_num'))
        # youtuber_keyword_queryset = Channel.objects.filter(l)
        result_page = paginator.paginate_queryset(channel_querysets, request)
        serializer = ChannelListSerializer(result_page, many=True)
        result=serializer.data
        additional_data = []
        for channel_queryset in channel_querysets:
            videos = channel_queryset.video.order_by('-upload_time')
            video_counts = len(videos)
            recent_videos = videos[:2]
            recent_video_url =[]
            for recent_video in recent_videos:
                recent_video_url.append(recent_video.thumbnail_url)

            max_views_count = list(channel_queryset.channelviews.order_by('-check_time')[:1])
            try:
                max_views_count= max_views_count[0].view_count
            except:
                max_views_count=0
            try:
                popularity = round(max_views_count / channel_queryset.subscriber_num, 1)
            except:
                popularity = 0
            additional_data.append({'video_counts':video_counts,'recent_videos':recent_video_url,'max_views_count':max_views_count,'popularity':popularity})

        for i in range(len(result)):
            result[i].update(additional_data[i])
        return paginator.get_paginated_response(result)
    else:
        paginator = PageNumberPagination()
        paginator.page_size = 10
        queryset = Channel.objects.all()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = ChannelListSerializer(result_page,many=True)
        return paginator.get_paginated_response(serializer.data)
      

    