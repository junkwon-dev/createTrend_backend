from .documents import VideoDocument
from elasticsearch_dsl import A
from .serializers import (
    TopVideoSerializer,
    RecentVideoSerializer,
    KeywordCountSerializer,
)
import itertools, collections
from rest_framework.response import Response


class Keyword(object):
    def __init__(self, keyword):
        self.name = keyword["name"]
        self.value = keyword["value"]


def search_keyword(keyword):
    # Elasticsearch query
    popular_top_keyword = (
        VideoDocument
            .search()
            .filter('match', videokeywordnews__keyword=keyword)
            .filter('range', popularity={'lt': 7})
            .filter('range', upload_time={'gte': 'now-14d/d', 'lt': "now"})
            .sort({"popularity": "desc"})[:100]
    )

    # 인기 비디오 5개 추출 및 직렬화
    top5_video = popular_top_keyword[:5]
    serialized_top5_video = TopVideoSerializer(top5_video, many=True)

    # 인기도 퍼센트화
    for video in serialized_top5_video.data:
        video['popularity'] = video['popularity'] * 100

    # 해당 키워드가 함께한 키워드들 모두 추출
    top_popular_keywords = []
    for popular_keyword in popular_top_keyword:
        keyword_tmp = [
            popular_keywords.keyword for popular_keywords in popular_keyword.videokeywordnews
        ]
        top_popular_keywords.append(keyword_tmp)

    # 최빈도 10개 키워드 추출
    top_popular_keywords = list(itertools.chain(*top_popular_keywords))
    counter = collections.Counter(top_popular_keywords)
    top_popular_keywords = dict(counter.most_common(n=10))
    top_popular_keywords = [
        {"name": key, "value": top_popular_keywords[key]} for key in top_popular_keywords.keys()
    ]
    top_popular_keywords = [Keyword(keyword=tmp_keyword) for tmp_keyword in top_popular_keywords]
    serialized_top_popular_keywords = KeywordCountSerializer(top_popular_keywords, many=True)

    # 영상화 추이
    imaging_transition = (
        VideoDocument
            .search()
            .filter('match', videokeywordnews__keyword=keyword)
            .filter('range', popularity={'lt': 7})
            .filter('range', upload_time={'gte': 'now-8d/d', 'lt': "now"})
    )
    imaging_transition.aggs.bucket('mola', A('date_histogram', field='upload_time', calendar_interval='1d'))
    response = imaging_transition.execute()
    imaging_transition_list = []
    for tag in response.aggregations.mola.buckets:
        imaging_transition_list.append({'date': tag.key_as_string[:10], 'value': tag.doc_count})

    # 인기도 추이
    popular_transition = (
        VideoDocument
            .search()
            .filter('match', videokeywordnews__keyword=keyword)
            .filter('range', upload_time={'gte': 'now-8d/d', 'lt': "now"})
    )
    popular_transition.aggs.bucket('mola', A('date_histogram', field='upload_time', calendar_interval='1d')) \
        .metric('popularity_per_day', A('avg', field='popularity'))
    response = popular_transition.execute()
    popular_transition_list = []
    for tag in response.aggregations.mola.buckets:
        if tag.popularity_per_day.value is not None:
            popular_transition_list.append(
                {'date': tag.key_as_string[:10], 'value': tag.popularity_per_day.value * 100})
        else:
            popular_transition_list.append({'date': tag.key_as_string[:10], 'value': 0})

    # 워드맵
    word_map_keyword_video = (
        VideoDocument
            .search()
            .filter('match', videokeywordnews__keyword=keyword)
            .filter('range', upload_time={'gte': 'now-14d/d', 'lt': "now"})
            .sort({"upload_time": "desc"})[:100]
    )
    word_map_keyword = []
    for video in word_map_keyword_video:
        keyword_tmp = [video_keyword.keyword for video_keyword in video.videokeywordnews]
        word_map_keyword.append(keyword_tmp)
    word_map_keyword = list(itertools.chain(*word_map_keyword))
    while keyword in word_map_keyword:
        word_map_keyword.remove(keyword)
    counter = collections.Counter(word_map_keyword)
    word_map_keyword = dict(counter.most_common(n=7))
    word_map_keyword = [{"name": key, "value": word_map_keyword[key]} for key in word_map_keyword.keys()]
    word_map_keyword = [Keyword(keyword=keyword_tmp) for keyword_tmp in word_map_keyword]
    serialized_word_map_keyword = KeywordCountSerializer(word_map_keyword, many=True)
    serialized_word_map_keyword = serialized_word_map_keyword.data

    # 워드맵 아이템 색 추가
    for item_index in range(len(serialized_word_map_keyword)):
        if item_index == 0:
            serialized_word_map_keyword[item_index].update({"color": "#f9bf69"})
        elif item_index == 1:
            serialized_word_map_keyword[item_index].update({"color": "#f65a5a"})
        elif item_index == 2:
            serialized_word_map_keyword[item_index].update({"color": "#508ddc"})
        elif item_index == 3:
            serialized_word_map_keyword[item_index].update({"color": "#f9bf69"})
        elif item_index == 4:
            serialized_word_map_keyword[item_index].update({"color": "#f65a5a"})
        else:
            serialized_word_map_keyword[item_index].update({"color": "#508ddc"})

    # 최근영상
    recent_video = (
        VideoDocument
            .search()
            .filter('match', videokeywordnews__keyword=keyword)
            .filter('range', popularity={'lt': 7})
            .filter('range', upload_time={'gte': 'now-14d/d', 'lt': "now"})
            .sort({"views_growth": "desc"})[:5]
    )

    # 최근 영상 직렬화
    serialized_recent_video = RecentVideoSerializer(recent_video, many=True)
    for video in serialized_recent_video.data:
        video['popularity'] = video['popularity'] * 100

    # 영상화 키워드
    top_imaging_video = (
        VideoDocument
            .search()
            .filter('match', videokeywordnews__keyword=keyword)
            .filter('range', upload_time={'gte': 'now-14d/d', 'lt': "now"})[:500]
    )

    # 최빈 키워드 10개 추출
    top_imaging_keyword = []
    for imaging_video in top_imaging_video:
        tmp_keyword = [
            imaging_keywords.keyword for imaging_keywords in imaging_video.videokeywordnews
        ]
        top_imaging_keyword.append(tmp_keyword)
    top_imaging_keyword = list(itertools.chain(*top_imaging_keyword))
    counter = collections.Counter(top_imaging_keyword)
    top_imaging_keyword = dict(counter.most_common(n=10))
    top_imaging_keyword = [
        {"name": key, "value": top_imaging_keyword[key]} for key in top_imaging_keyword.keys()
    ]
    top_imaging_keyword = [Keyword(keyword=tmp_keyword) for tmp_keyword in top_imaging_keyword]
    serialized_top_imaging_keyword = KeywordCountSerializer(top_imaging_keyword, many=True)
    return Response(
        {
            "video": [
                {"type": "analysis", "data": serialized_recent_video.data},
                {"type": "aside", "data": serialized_top5_video.data},
            ],  # 최신
            "wordmap": {
                "name": keyword,
                "color": "#666",
                "children": serialized_word_map_keyword,
            },
            "lines": [
                {"type": "영상화 추이", "data": imaging_transition_list},
                {"type": "인기도 추이", "data": popular_transition_list},
            ],
            "keyword": [
                {"type": "인기 키워드", "keyword": serialized_top_popular_keywords.data},
                {
                    "type": "영상화 키워드",
                    "keyword": serialized_top_imaging_keyword.data
                },
            ],
        }
    )
