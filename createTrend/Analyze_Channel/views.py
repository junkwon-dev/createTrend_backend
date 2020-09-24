from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import F, Count, Sum, Max
from django.db.models.functions import Coalesce
import datetime, itertools, collections, time
from .models import Channel, VideoKeywordNew, Video, ChannelSubscriber, VideoViews
from .serializers import VideoKeywordSerializer, KeywordCountSerializer, VideoSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

param_keyword_data_search_hint = openapi.Parameter(
    'search',
    openapi.IN_QUERY,
    description='영상화 혹은 인기 키워드를 검색합니다. 영상화 혹은 인기 를 입력하세요.',
    type=openapi.TYPE_STRING
)
param_keyword_data_keyword_hint = openapi.Parameter(
    'keyword',
    openapi.IN_QUERY,
    description='검색하고 싶은 키워드를 입력하세요.',
    type=openapi.TYPE_STRING
)


@swagger_auto_schema(method='get', manual_parameters=[param_keyword_data_search_hint, param_keyword_data_keyword_hint])
@api_view(['GET'])
def keyword_data(request):
    '''
    전체 채널 인기,영상화 TOP10 키워드 API
    ---
    전체 채널 TOP10 키워드를 클릭할 때 키워드의 인기도, 영상화 수치, 추이 등을 제공하는 API입니다.
    '''
    search = request.query_params.get('search')
    keyword = request.query_params.get('keyword')
    if (search == '영상화' and keyword):
        start_time = time.time()
        # weekAvgIncrease,dayAvgIncrease=imagingIncreaseRate(keyword)
        start = timezone.now() - datetime.timedelta(days=14)
        start = start.strftime("%Y-%m-%d")
        end = timezone.now().strftime("%Y-%m-%d")

        imagingTransition = list(Video.objects \
                                 .filter(videokeywordnew__keyword__contains=keyword, upload_time__range=(start, end)) \
                                 .extra(select={'date': "TO_CHAR(upload_time, 'YYYY-MM-DD')"}).values('date') \
                                 .annotate(value=Count('idx')))
        imagingVideoSum = 0
        for imagingvideo in imagingTransition:
            imagingVideoSum += imagingvideo['value']
        try:
            avgImaging = imagingVideoSum / len(imagingTransition)
        except:
            avgImaging = 0
        keywordVideo = Video.objects \
                           .filter(videokeywordnew__keyword__contains=keyword, upload_time__range=(start, end)) \
                           .order_by('-upload_time')[:1000].prefetch_related('videokeywordnew')
        keywords = []
        for video in keywordVideo:
            videokeytmp = [videokeyword.keyword for videokeyword in video.videokeywordnew.all()]
            keywords.append(videokeytmp)
        keywords = list(itertools.chain(*keywords))
        # while keyword in keywords:
        #     keywords.remove(keyword)
        counter = collections.Counter(keywords)
        keywords = dict(counter.most_common(n=6))
        keywords = [{"name": key, "value": keywords[key]} for key in keywords.keys()]

        class Keyword(object):
            def __init__(self, keyword):
                self.name = keyword['name']
                self.value = keyword['value']

        keywords = [Keyword(keyword=keyword) for keyword in keywords]
        keywordCountSerializer = KeywordCountSerializer(keywords, many=True)
        topViewVideo = Video.objects.filter(videokeywordnew__keyword=keyword, upload_time__range=(start, end)) \
                           .order_by('-views')[:5]
        topViewVideoSerializer = VideoSerializer(topViewVideo, many=True)
        # return Response([imagingTransition,keywordCountSerializer.data])
        wordmapItems = keywordCountSerializer.data
        # 색깔추가
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
        end_time = time.time() - start_time
        print(f'response time : {end_time}')
        return Response({"type": "영상", "keyword": [{"name": keyword, "popular": avgImaging, "wordmap": {"name": keyword,
                                                                                                        "children": wordmapItems},
                                                    "lines": {'type': "영상화 추이", 'data': imagingTransition},
                                                    "video": {"type": "analysis",
                                                              "data": topViewVideoSerializer.data}}]})
    elif (search == '인기' and keyword):

        start_time = time.time()
        start = timezone.now() - datetime.timedelta(days=30)
        start = start.strftime("%Y-%m-%d")
        end = timezone.now().strftime("%Y-%m-%d")
        popularTransitionQuery = list(Video.objects \
                                      .filter(videokeywordnew__keyword__contains=keyword,
                                              upload_time__range=(start, end), popularity__isnull=False)
                                      .extra(select={'date': "TO_CHAR(upload_time, 'YYYY-MM-DD')"}).values('date')
                                      .annotate(value=Coalesce(Sum('popularity'), 0)))

        subscribers = {}
        popularTransition = []
        popularDictSum = 0
        for subdictKey in popularTransitionQuery:
            print(subdictKey['date'], subdictKey['value'])
            popularTransition.append({"date": subdictKey['date'], "value": subdictKey['value']})
            try:
                popularDictSum += subdictKey['value']
            except:
                pass
        try:
            avgPopularDict = popularDictSum / len(popularTransitionQuery)
        except:
            avgPopularDict = 0
        keywordVideo = Video.objects \
                           .filter(videokeywordnew__keyword__contains=keyword, upload_time__range=(start, end)) \
                           .order_by('-upload_time')[:500].prefetch_related('videokeywordnew')
        keywords = []
        for video in keywordVideo:
            videokeytmp = [videokeyword.keyword for videokeyword in video.videokeywordnew.all()]
            keywords.append(videokeytmp)
        keywords = list(itertools.chain(*keywords))
        # while keyword in keywords:
        #     keywords.remove(keyword)
        counter = collections.Counter(keywords)
        keywords = dict(counter.most_common(n=7))
        keywords = [{"name": key, "value": keywords[key]} for key in keywords.keys()]
        end_time = time.time() - start_time
        print(f'response time : {end_time}')

        class Keyword(object):
            def __init__(self, keyword):
                self.name = keyword['name']
                self.value = keyword['value']

        keywords = [Keyword(keyword=keyword) for keyword in keywords]

        popularVideo = Video.objects.filter(
            upload_time__range=(start, end)
        ).order_by(F('popularity').desc(nulls_last=True))[:5]
        # .order_by(F('popularity').desc(nulls_last=True))[:5]
        popularVideoSerializer = VideoSerializer(popularVideo, many=True)

        keywordCountSerializer = KeywordCountSerializer(keywords, many=True)
        end_time = time.time() - start_time
        print(f'response time : {end_time}')
        wordmapItems = keywordCountSerializer.data
        # 색깔추가
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
        # return Response([popularDict,keywordCountSerializer.data])
        return Response({"type": "인기", "keyword": [{"name": keyword, "popular": avgPopularDict,
                                                    "wordmap": {"name": keyword,
                                                                "children": wordmapItems},
                                                    "lines": {"type": "인기도 추이", "data": popularTransition},
                                                    "video": {"type": "analysis",
                                                              "data": popularVideoSerializer.data}}]})

    return Response("")


@api_view(['GET'])
def analyze_channel(request):
    '''
    전체 채널 인기,영상화 TOP10 키워드 API
    ---
    전체 채널 중 인기, 영상화 TOP 10 키워드를 제공하는 API입니다.
    '''
    start_time = time.time()
    search = None
    start = timezone.now() - datetime.timedelta(days=14)
    start = start.strftime("%Y-%m-%d")
    end = timezone.now().strftime("%Y-%m-%d")

    class Keyword(object):
        def __init__(self, keyword):
            self.name = keyword['name']
            self.value = keyword['value']

    popularTopKeyword = list(Video.objects.prefetch_related('videokeywordnew') \
                             .filter(upload_time__range=(start, end)) \
                             .order_by(F('popularity').desc(nulls_last=True))[:300])
    topPopularKeywords = []

    for popularKeyword in popularTopKeyword:
        # print(VideoKeywordNew.objects.filter(video_idx=popularKeyword.idx))
        keyword = [keywords.keyword for keywords in popularKeyword.videokeywordnew.all()]
        topPopularKeywords.append(keyword)
    topPopularKeywords = list(itertools.chain(*topPopularKeywords))
    counter = collections.Counter(topPopularKeywords)
    topPopularKeywords = dict(counter.most_common(n=10))
    topPopularKeywords = [{"name": key, "value": topPopularKeywords[key]} for key in topPopularKeywords.keys()]
    topPopularKeywords = [Keyword(keyword=keyword) for keyword in topPopularKeywords]
    # 영상화 키워드
    start = timezone.now() - datetime.timedelta(days=7)
    start = start.strftime("%Y-%m-%d")
    end = timezone.now().strftime("%Y-%m-%d")
    imagingTransitionKeyword = list(Video.objects.prefetch_related('videokeywordnew') \
                                    .filter(upload_time__range=(start, end)) \
                                    .order_by(F('upload_time').desc(nulls_last=True))[:100])
    topImagingKeywords = []
    for imagingkeywordvideo in imagingTransitionKeyword:
        keyword = [keywords.keyword for keywords in imagingkeywordvideo.videokeywordnew.all()]
        topImagingKeywords.append(keyword)
    end_time = time.time() - start_time
    print(f'response time : {end_time}')
    topImagingKeywords = list(itertools.chain(*topImagingKeywords))
    counter = collections.Counter(topImagingKeywords)
    topImagingKeywords = dict(counter.most_common(n=10))

    topImagingKeywords = [{"name": key, "value": topImagingKeywords[key]} for key in topImagingKeywords.keys()]
    topImagingKeywords = [Keyword(keyword=keyword) for keyword in topImagingKeywords]

    topImagingKeywordCountSerializer = KeywordCountSerializer(topImagingKeywords, many=True)
    topkeywordCountSerializer = KeywordCountSerializer(topPopularKeywords, many=True)
    end_time = time.time() - start_time
    print(f'response time : {end_time}')
    return Response([{"type": "인기", "keyword": topkeywordCountSerializer.data},
                     {"type": "영상화", "keyword": topImagingKeywordCountSerializer.data}])
