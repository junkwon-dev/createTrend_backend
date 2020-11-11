from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime, timedelta
from .serializers import ChannelInfoSerializer, ChannelSubscriberSerializer, ChannelListSerializer \
    , VideoSerializer, VideoViewsSerializer, VideoKeywordNewSerializer, KeywordCountSerializer \
    , ChannelViewsCountSerializer
from rest_framework.pagination import PageNumberPagination
from .models import Channel, ChannelSubscriber, VideoViews, Video
from itertools import chain
from django.db.models import Max
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import collections, itertools, datetime


class Keyword(object):
    def __init__(self, keyword):
        self.name = keyword['name']
        self.value = keyword['value']

@api_view(['GET'])
def channel_info(request, pk):
    '''
    채널 정보 API
    ---
    해당되는 채널의 정보, 채널을 분석해서 제공하는 API입니다.
    '''

    # 채널 객체가 없으면 404 response
    try:
        channel = Channel.objects \
            .get(pk=pk)
    except Channel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # 해달 채널의 비디오를 일자별로 묶음
    videos = channel.video \
        .annotate(hottest_video_made_at=Max('videoviews__check_time'))
    hottest_videos = channel.video.order_by('-views')[:5]

    channel_subscriber = channel.channelsubscriber \
                               .order_by('-check_time')[:1]
    videos = channel.video.prefetch_related('videokeywordnew')[:50]

    # 워드맵 데이터 추출
    keywords = []
    for video in videos.iterator():
        keyword = [vk.keyword for vk in video.videokeywordnew.all()]
        keywords.append(keyword)
    channel_name = channel.channel_name
    keywords = list(itertools.chain(*keywords))
    while channel_name in keywords:
        keywords.remove(channel_name)
    counter = collections.Counter(keywords)
    keywords = dict(counter.most_common(n=7))
    keywords = [{"name": key, "value": keywords[key]} for key in keywords.keys()]

    class Keyword(object):
        def __init__(self, keyword):
            self.name = keyword['name']
            self.value = keyword['value']

    keywords = [Keyword(keyword=keyword) for keyword in keywords]
    start = timezone.now() - datetime.timedelta(days=50)
    start = start.strftime("%Y-%m-%d")
    end = timezone.now().strftime("%Y-%m-%d")
    channel_subscribers = list(
        channel.channelsubscriber.filter(check_time__range=(start, end)).order_by('check_time'))
    channel_subscriber_transition = []
    for channel_subscirber in channel_subscribers:
        date = channel_subscirber.check_time
        value = channel_subscirber.subscriber_num
        date_value = str(date)[:10]
        channel_subscriber_transition.append({"date": date_value, "value": value})

    # 데이터 직렬화
    keywordCountSerializer = KeywordCountSerializer(keywords, many=True)
    serialized_channel_subscriber = ChannelSubscriberSerializer(channel_subscriber, many=True)
    channelSerializer = ChannelInfoSerializer(channel)
    topViewVideoSerializer = VideoSerializer(hottest_videos, many=True)
    subscriber_number = serialized_channel_subscriber.data[0]['subscriber_num']
    channelinfodict = channelSerializer.data
    channelinfodict['subscriber'] = subscriber_number
    wordmapItems = keywordCountSerializer.data

    #워드맵 데이터 색 추가
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
    return Response({'channelInfo': channelinfodict, 'video': {"type": "aside", "data": topViewVideoSerializer.data} \
                        , 'keyword': {'pie': keywordCountSerializer.data},
                     'wordmap': {'name': channel_name, 'color': '#666', 'children': wordmapItems},
                     'line': {"type": "구독자수 추이", "data": channel_subscriber_transition}})


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


@swagger_auto_schema(method='get',
                     manual_parameters=[param_channelperioddata_start_hint, param_channelperioddata_end_hint])
@api_view(['GET'])
def channel_period_data(request, pk):
    '''
    채널의 기간 내 DATA API
    ---
    해당 채널에서 기간을 설정하면 그 기간 내 인기 영상, 구독자 수 추이 등을 제공하는 API입니다.
    '''
    try:
        channel = Channel.objects \
            .get(pk=pk)
    except Channel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        start = request.query_params.get('start')
        end = request.query_params.get('end')
        if (start and end):
            # 기간 내의 데이터를 조회수 급상승으로 정렬해서 조회수 급상승 영상을 추출한다.
            hottest_videos = (channel.video.filter(upload_time__range=(start, end)).order_by('-views_growth'))
            keyword_videos = hottest_videos[:50]
            hottest_videos = hottest_videos[:5]
            keywords = []

            # 워드맵 데이터 추출
            for video in keyword_videos:
                keyword = [vk.keyword for vk in video.videokeywordnew.all()]
                keywords.append(keyword)
            keywords = list(itertools.chain(*keywords))
            channel_name = channel.channel_name
            while channel_name in keywords:
                keywords.remove(channel_name)
            counter = collections.Counter(keywords)
            keywords = dict(counter.most_common(n=7))
            keywords = [{"name": key, "value": keywords[key]} for key in keywords.keys()]
            keywords = [Keyword(keyword=keyword) for keyword in keywords]

            # 직렬화
            keywordCountSerializer = KeywordCountSerializer(keywords, many=True)
            videoSerializer = VideoSerializer(hottest_videos, many=True)
            wordmapItems = keywordCountSerializer.data

            # 워드맵 데이터 색 추가
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
            return Response({'video': {"type": "analysis", "data": videoSerializer.data},
                             'keyword': {'pie': keywordCountSerializer.data},
                             'wordmap': {'name': channel_name, 'color': '#666', 'children': wordmapItems}})
        else:
            start = timezone.now() - datetime.timedelta(days=14)
            start = start.strftime("%Y-%m-%d")
            end = timezone.now().strftime("%Y-%m-%d")
            channelSubscriber = channel.channelsubscriber.filter(check_time__range=(start, end))
            channelSubscriberSerializer = ChannelSubscriberSerializer(channelSubscriber, many=True)
            return Response(channelSubscriberSerializer.data)


@api_view(['GET'])
def channel_list(request):
    '''
    채널리스트 API
    ---
    전체 채널의 목록을 보여주는 API입니다.
    '''
    youtuber_name = request.query_params.get('youtuber_name')

    if youtuber_name is not None:
        # 유튜버 검색 기능
        paginator = PageNumberPagination()
        paginator.page_size = 10
        channel_querysets = list(Channel.objects.prefetch_related('video', 'channelviews').filter(
            channel_name__icontains=youtuber_name).order_by('-subscriber_num'))

        # 데이터 많을 시 페이지네이션 진행(페이지별로 데이터 끊기)
        result_page = paginator.paginate_queryset(channel_querysets, request)

        # 데이터 직렬화
        serializer = ChannelListSerializer(result_page, many=True)
        result = serializer.data
        additional_data = []
        for channel_queryset in channel_querysets:
            videos = channel_queryset.video.order_by('-upload_time')
            video_counts = len(videos)
            recent_videos = videos[:2]
            recent_video_url = []
            for recent_video in recent_videos:
                recent_video_url.append(recent_video.thumbnail_url)

            max_views_count = list(channel_queryset.channelviews.order_by('-check_time')[:1])
            try:
                max_views_count = max_views_count[0].view_count
            except:
                max_views_count = 0
            try:
                popularity = round(max_views_count / channel_queryset.subscriber_num, 1)
            except:
                popularity = 0
            additional_data.append(
                {'video_counts': video_counts, 'recent_videos': recent_video_url, 'max_views_count': max_views_count,
                 'popularity': popularity})

        for i in range(len(result)):
            result[i].update(additional_data[i])
        return paginator.get_paginated_response(result)
    else:
        paginator = PageNumberPagination()
        paginator.page_size = 10
        queryset = Channel.objects.all()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = ChannelListSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
