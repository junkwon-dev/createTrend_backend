import django

django.setup()
from rest_framework.decorators import api_view
from django.utils import timezone
from datetime import datetime
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count, Sum
from Search_Keyword.serializers import (
    VideoKeywordSerializer,
    TopVideoSerializer,
    RecentVideoSerializer,
    KeywordCountSerializer,
)
from .models import VideoKeywordNew, Video
from rest_framework.response import Response
import datetime, itertools, collections, time
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django import db
from django.db.models.functions import Coalesce
from multiprocessing import Manager, Process
from .documents import VideoDocument
from elasticsearch_dsl import Q,A

param_search_hint = openapi.Parameter(
    "search", openapi.IN_QUERY, description="검색하고 싶은 키워드를 입력하세요.", type=openapi.TYPE_STRING,
)


class Keyword(object):
    def __init__(self, keyword):
        self.name = keyword["name"]
        self.value = keyword["value"]



@swagger_auto_schema(method="get", manual_parameters=[param_search_hint])
@api_view(["GET"])
def keyword(request):
    """
    키워드 검색 API
    ---
    검색한 키워드와 관련된 최근 영상과, 인기있는 영상, 관련 키워드 워드맵 정보 등을 제공하는 api입니다.
    """
    start_time = time.time()
    search = request.query_params.get("search")
    if search:
        start = timezone.now() - datetime.timedelta(days=14)
        start = start.strftime("%Y-%m-%d")
        end = timezone.now().strftime("%Y-%m-%d")
        popularTopKeyword=(
            VideoDocument
            .search()
            .filter('match', videokeywordnews__keyword=search)
            .filter('range', popularity={'lt':7})
            .filter('range', upload_time={'gte':'now-14d/d','lt':"now"})
            .sort({"popularity":"desc"})[:100]
        )
        topVideo = popularTopKeyword[:5]
        topVideoSerializer = TopVideoSerializer(topVideo, many=True)
        for video in topVideoSerializer.data:
            video['popularity']=video['popularity']*100
        topPopularKeywords = []
        for popularKeyword in popularTopKeyword:
            # print(popularKeyword.videokeywordnew.all())
            keyword = [
                popkeywords.keyword for popkeywords in popularKeyword.videokeywordnews
            ]
            topPopularKeywords.append(keyword)
        topPopularKeywords = list(itertools.chain(*topPopularKeywords))
        counter = collections.Counter(topPopularKeywords)
        topPopularKeywords = dict(counter.most_common(n=10))
        topPopularKeywords = [
            {"name": key, "value": topPopularKeywords[key]} for key in topPopularKeywords.keys()
        ]
        topPopularKeywords = [Keyword(keyword=keyword) for keyword in topPopularKeywords]
        topkeywordCountSerializer = KeywordCountSerializer(topPopularKeywords, many=True)
        imagingTransition=(
        VideoDocument
            .search()
            .filter('match', videokeywordnews__keyword=search)
            .filter('range', popularity={'lt':7})
            .filter('range',upload_time={'gte':'now-8d/d','lt':"now"})
        )
        imagingTransition.aggs.bucket('mola',A('date_histogram',field='upload_time',calendar_interval='1d'))
        response=imagingTransition.execute()
        imagingTransitionList=[]
        for tag in response.aggregations.mola.buckets:
            imagingTransitionList.append({'date':tag.key_as_string[:10],'value':tag.doc_count})
        # 인기도추이
        popularTransition=(
        VideoDocument
            .search()
            .filter('match', videokeywordnews__keyword=search)
            .filter('range',upload_time={'gte':'now-8d/d','lt':"now"})
        )
        popularTransition.aggs.bucket('mola',A('date_histogram',field='upload_time',calendar_interval='1d'))\
            .metric('popularity_per_day', A('avg', field='popularity'))
        response=popularTransition.execute()
        popularTransitionList=[]
        print(response)
        for tag in response.aggregations.mola.buckets:
            if tag.popularity_per_day.value is not None:
                popularTransitionList.append({'date':tag.key_as_string[:10],'value':tag.popularity_per_day.value*100})
            else:
                popularTransitionList.append({'date':tag.key_as_string[:10],'value':0})

        #워드맵
        keyword_video=(
            VideoDocument
            .search()
            .filter('match', videokeywordnews__keyword=search)
            .filter('range',upload_time={'gte':'now-14d/d','lt':"now"})
            .sort({"upload_time":"desc"})[:100]
        )
        keywords = []
        for video in keyword_video:
            keyword = [videokeyword.keyword for videokeyword in video.videokeywordnews]
            keywords.append(keyword)
        keywords = list(itertools.chain(*keywords))
        while search in keywords:
            keywords.remove(search)
        counter = collections.Counter(keywords)
        keywords = dict(counter.most_common(n=7))
        keywords = [{"name": key, "value": keywords[key]} for key in keywords.keys()]
        keywords = [Keyword(keyword=keyword) for keyword in keywords]
        keywordCountSerializer = KeywordCountSerializer(keywords, many=True)
        wordmapItems = keywordCountSerializer.data
        # 색깔추가
        for itemIndex in range(len(wordmapItems)):
            if itemIndex == 0:
                wordmapItems[itemIndex].update({"color": "#f9bf69"})
            elif itemIndex == 1:
                wordmapItems[itemIndex].update({"color": "#f65a5a"})
            elif itemIndex == 2:
                wordmapItems[itemIndex].update({"color": "#508ddc"})
            elif itemIndex == 3:
                wordmapItems[itemIndex].update({"color": "#f9bf69"})
            elif itemIndex == 4:
                wordmapItems[itemIndex].update({"color": "#f65a5a"})
            else:
                wordmapItems[itemIndex].update({"color": "#508ddc"})

        #최근영상
        recent_video=(
            VideoDocument
            .search()
            .filter('match', videokeywordnews__keyword=search)
            .filter('range', popularity={'lt':7})
            .filter('range',upload_time={'gte':'now-14d/d','lt':"now"})
            .sort({"views_growth":"desc"})[:5]
        )

        recentVideoSerializer = RecentVideoSerializer(recent_video, many=True)
        for video in recentVideoSerializer.data:
            video['popularity']=video['popularity']*100


        # 인기키워드
        topImagingKeywordQuery=(
            VideoDocument
            .search()
            .filter('match', videokeywordnews__keyword=search)
            .filter('range',upload_time={'gte':'now-14d/d','lt':"now"})
        )
        topImagingKeywords = []
        for imagingkeywordvideo in topImagingKeywordQuery:
            keyword = [
                imagingkeywords.keyword for imagingkeywords in imagingkeywordvideo.videokeywordnews
            ]
            topImagingKeywords.append(keyword)
        topImagingKeywords = list(itertools.chain(*topImagingKeywords))
        counter = collections.Counter(topImagingKeywords)
        topImagingKeywords = dict(counter.most_common(n=10))
        topImagingKeywords = [
            {"name": key, "value": topImagingKeywords[key]} for key in topImagingKeywords.keys()
        ]
        topImagingKeywords = [Keyword(keyword=keyword) for keyword in topImagingKeywords]
        topImagingKeywordCountSerializer = KeywordCountSerializer(topImagingKeywords, many=True)
        return Response(
            {
                "video": [
                    {"type": "analysis", "data": recentVideoSerializer.data},
                    {"type": "aside", "data": topVideoSerializer.data},
                ],  # 최신
                "wordmap": {
                    "name": search,
                    "color": "#666",
                    "children": wordmapItems,
                },
                "lines": [
                    {"type": "영상화 추이", "data": imagingTransitionList},
                    {"type": "인기도 추이", "data": popularTransitionList},
                ],
                "keyword": [
                    {"type": "인기 키워드", "keyword": topkeywordCountSerializer.data},
                    {
                        "type": "영상화 키워드",
                        "keyword": topImagingKeywordCountSerializer.data
                    },
                ],
            }
        )
    else:
        paginator = PageNumberPagination()
        paginator.page_size = 10
        queryset = VideoKeywordNew.objects.all()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = VideoKeywordSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
