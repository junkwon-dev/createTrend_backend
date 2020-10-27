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

# from Search_Keyword.serializers import topComment
# Create your views here.
# class topCommentViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
param_search_hint = openapi.Parameter(
    "search", openapi.IN_QUERY, description="검색하고 싶은 키워드를 입력하세요.", type=openapi.TYPE_STRING,
)


class Keyword(object):
    def __init__(self, keyword):
        self.name = keyword["name"]
        self.value = keyword["value"]


def plus(search, start, end, return_dict, start_time):
    end_time = time.time() - start_time
    print(f"topVideoSerializer start time : {end_time}")

    # imagingTransition = dict(
    #     Video.objects
    #     .filter(
    #         videokeywordnew__keyword__regex=rf"(^| +){search}($| +)",
    #         upload_time__range=(start, end),
    #     )
    #     .distinct()
    #     .extra(select={"date": "TO_CHAR(upload_time, 'YYYY-MM-DD')"})
    #     .order_by("date")
    #     .values("date")
    #     .annotate(value=Count("idx"))
    # )
    imagingTransition=(
        VideoDocument
        .search()
        .filter('nested',path='videokeywordnews',query=Q('term', videokeywordnews__keyword=search))
        .filter('range',upload_time={'gte':'now-14d/d','lt':"now"})
    )
    imagingTransition.aggs.bucket('mola',A('date_histogram',field='upload_time',calendar_interval='1d'))
    imagingTransition=imagingTransition.execute()
    imagingTransitionList=[]
    for tag in imagingTransition.aggregations.mola.buckets:
        imagingTransitionList.append({'date':tag.key_as_string[:10],'count':tag.doc_count})
    popularTransitionQuery = list(
        Video.objects.filter(
            videokeywordnew__keyword__regex=rf"(^| +){search}($| +)",
            upload_time__range=(start, end),
            popularity__isnull=False,
        )
        .distinct()
        .extra(select={"date": "TO_CHAR(upload_time, 'YYYY-MM-DD')"})
        .order_by("-date")
        .values("date")
        .annotate(value=Coalesce(Sum("popularity"), 0))
    )
    popularTransitionQuery=(
        VideoDocument
        .search()
        .filter('nested',path='videokeywordnews',query=Q('term', videokeywordnews__keyword=search))
        .filter('range',upload_time={'gte':'now-14d/d','lt':"now"})
    )
    popularTransitionQuery.aggs.bucket('mola',A('avg',field='upload_time',calendar_interval='1d'))
    popularTransitionQuery=popularTransitionQuery.execute()()
    popularTransitionQuery=[]
    for tag in imagingTransition.aggregations.mola.buckets:
        imagingTransitionList.append({'date':tag.key_as_string[:10],'count':tag.doc_count})

    subscribers = []

    for subdict in popularTransitionQuery:
        subscribers.append({"date": subdict["date"], "value": round(subdict["value"] * 100, 1)})

    return_dict["imagingTransition"] = imagingTransitionList
    return_dict["subscribers"] = subscribers

    end_time = time.time() - start_time
    print(f"plus response time : {end_time}")
    print(imagingTransitionList)


def recentVideoSerializer(search, start, end, return_dict, start_time):
    end_time = time.time() - start_time
    print(f"recentVideoSerializer start time : {end_time}")

    # recent_video = (
    #     Video.objects
    #     .filter(
    #         videokeywordnew__keyword__regex=rf"(^| +){search}($| +)",
    #         upload_time__range=(start, end),
    #         views_growth__isnull=False
    #     )
    #     .distinct()
    #     .order_by("-views_growth")[:5]
    # )
    recent_video=(
        VideoDocument
        .search()
        .filter('nested',path='videokeywordnews',query=Q('term', videokeywordnews__keyword=search))
        .filter('range',upload_time={'gte':'now-14d/d','lt':"now"})
        .sort({"views_growth":"desc"})[:5]
    )
    
    recentVideoSerializer = RecentVideoSerializer(recent_video, many=True)
    for video in recentVideoSerializer.data:
        video['popularity']=video['popularity']*100
    return_dict["recentVideoSerializer_data"] = recentVideoSerializer.data
    print(return_dict["recentVideoSerializer_data"])

    end_time = time.time() - start_time
    print(f"recentVideoSerializer response time : {end_time}")


def wordmapItems(search, start, end, return_dict, start_time):
    end_time = time.time() - start_time
    print(f"wordmapItems start time : {end_time}")

    # keyword_video = (
    #     Video.objects.prefetch_related("videokeywordnew")
    #     .filter(
    #         videokeywordnew__keyword__regex=rf"(^| +){search}($| +)",
    #         upload_time__range=(start, end),
    #     )
    #     .order_by("-upload_time")[:100]
    # )
    keyword_video=(
        VideoDocument
        .search()
        .filter('nested',path='videokeywordnews',query=Q('term', videokeywordnews__keyword=search))
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

    return_dict["wordmapItems"] = wordmapItems

    end_time = time.time() - start_time
    print(f"wordmapItems response time : {end_time}")


def topImagingKeywordCountSerializer(search, start, end, return_dict, start_time):
    end_time = time.time() - start_time
    print(f"topImagingKeywordCountSerializer start time : {end_time}")

    # imagingTransitionKeyword = list(
    #     Video.objects.prefetch_related("videokeywordnew").filter(
    #         videokeywordnew__keyword__regex=rf"(^| +){search}($| +)",
    #         upload_time__range=(start, end),
    #     )
    # )

    imagingTransitionKeyword=(
        VideoDocument
        .search()
        .filter('nested',path='videokeywordnews',query=Q('term', videokeywordnews__keyword=search))
        .filter('range',upload_time={'gte':'now-14d/d','lt':"now"})
    )
    topImagingKeywords = []
    for imagingkeywordvideo in imagingTransitionKeyword:
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

    return_dict["topImagingKeywordCountSerializer_data"] = topImagingKeywordCountSerializer.data

    end_time = time.time() - start_time
    print(f"topImagingKeywordCountSerializer response time : {end_time}")


@swagger_auto_schema(method="get", manual_parameters=[param_search_hint])
@api_view(["GET"])
def keyword(request):
    """
    키워드 검색 API
    ---
    검색한 키워드와 관련된 최근 영상과, 인기있는 영상, 관련 키워드 워드맵 정보 등을 제공하는 api입니다.
    """
    if request.method == "GET":
        start_time = time.time()
        search = request.query_params.get("search")
        if search:
            start = timezone.now() - datetime.timedelta(days=14)
            start = start.strftime("%Y-%m-%d")
            end = timezone.now().strftime("%Y-%m-%d")

            db.connections.close_all()

            manager = Manager()
            data_dict = manager.dict()

            # p1 = Process(target=plus, args=(search, start, end, data_dict, start_time))
            p2 = Process(
                target=recentVideoSerializer, args=(search, start, end, data_dict, start_time),
            )
            p3 = Process(target=wordmapItems, args=(search, start, end, data_dict, start_time))
            p4 = Process(
                target=topImagingKeywordCountSerializer,
                args=(search, start, end, data_dict, start_time),
            )

            # p1.start()
            p2.start()
            p3.start()
            p4.start()

            # popularTopKeyword = (
            #     Video.objects.filter(
            #         videokeywordnew__keyword__regex=rf"(^| +){search}($| +)",
            #         upload_time__range=(start, end)
            #     )
            #     .order_by("-popularity")
            #     .distinct()
            #     .prefetch_related("videokeywordnew")[:100]
            # )

            popularTopKeyword=(
                VideoDocument
                .search()
                .filter('nested',path='videokeywordnews',query=Q('term', videokeywordnews__keyword=search))
                .filter('range',upload_time={'gte':'now-14d/d','lt':"now"})
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

            end_time = time.time() - start_time
            print(f"response time : {end_time}")

            # p1.join()
            p2.join()
            p3.join()
            p4.join()

            end_time = time.time() - start_time
            print(f"result time : {end_time}")
            imagingTransition=(
            VideoDocument
                .search()
                .filter('nested',path='videokeywordnews',query=Q('term', videokeywordnews__keyword=search))
                .filter('range',upload_time={'gte':'now-14d/d','lt':"now"})
            )
            imagingTransition.aggs.bucket('mola',A('date_histogram',field='upload_time',calendar_interval='1d'))
            response=imagingTransition.execute()
            imagingTransitionList=[]
            # print(response)
            for tag in response.aggregations.mola.buckets:
                imagingTransitionList.append({'date':tag.key_as_string[:10],'count':tag.doc_count})
                
                
            #인기도추이
            # popularTransition=(
            # VideoDocument
            #     .search()
            #     .filter('nested',path='videokeywordnews',query=Q('term', videokeywordnews__keyword=search))
            #     .filter('range',upload_time={'gte':'now-14d/d','lt':"now"})
            # )
            # imagingTransition.aggs.bucket('mola',A('date_histogram',field='upload_time',calendar_interval='1d'))
            # response=imagingTransition.execute()
            # imagingTransitionList=[]
            # print(response)
            for tag in response.aggregations.mola.buckets:
                imagingTransitionList.append({'date':tag.key_as_string[:10],'count':tag.doc_count})    
            
            return Response(
                {
                    "video": [
                        {"type": "analysis", "data": data_dict["recentVideoSerializer_data"],},
                        {"type": "aside", "data": topVideoSerializer.data},
                    ],  # 최신
                    "wordmap": {
                        "name": search,
                        "color": "#666",
                        "children": data_dict["wordmapItems"],
                    },
                    "lines": [
                        {"type": "영상화 추이", "data": imagingTransitionList},
                        # {"type": "인기도 추이", "data": data_dict["subscribers"]},
                    ],
                    "keyword": [
                        {"type": "인기 키워드", "keyword": topkeywordCountSerializer.data},
                        {
                            "type": "영상화 키워드",
                            "keyword": data_dict["topImagingKeywordCountSerializer_data"],
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
