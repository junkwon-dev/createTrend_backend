from .documents import VideoDocument
from elasticsearch_dsl import Q, A
import datetime, itertools, collections, time
from rest_framework.response import Response
from .models import Channel, VideoKeywordNew, Video, ChannelSubscriber, VideoViews
from .serializers import VideoKeywordSerializer, KeywordCountSerializer, VideoSerializer


#키워드객체입니다.
class Keyword(object):
    def __init__(self, keyword):
        self.name = keyword['name']
        self.value = keyword['value']


#Elasticsearch에 해당 키워드가 영상화 된 최근 7일치 데이터를 일자별로 질의 후 가공, 리스트로 반환하는 함수입니다.
def get_imaging_transition(keyword):
    #Elasticsearch query입니다.
    query_imaging_transition = (
        VideoDocument
            .search()
            .filter('match', videokeywordnews__keyword=keyword)
            .filter('range', popularity={'lt': 7})
            .filter('range', upload_time={'gte': 'now-8d/d', 'lt': "now"})
    )
    #aggregation bucket 메소드를 이용하여 날짜별로 데이터를 집합(count)합니다.
    query_imaging_transition.aggs.bucket('mola', A('date_histogram', field='upload_time', calendar_interval='1d'))
    response = query_imaging_transition.execute()
    imaging_transition_list = []
    for tag in response.aggregations.mola.buckets:
        imaging_transition_list.append({'date': tag.key_as_string[:10], 'value': tag.doc_count})
    return imaging_transition_list


#추이 비디오의 {인기도, 영상화} 합계를 구하는 함수입니다.
def get_video_sum(transition_list):
    video_sum = 0
    for video in transition_list:
        video_sum += video['value']
    return video_sum


#추이 비디오의 {인기도, 영상화} 평균을 구하는 함수입니다.
def get_video_avg(video_sum,counts_of_video):
    try:
        video_avg = video_sum / counts_of_video
    except:
        video_avg = 0
    return video_avg


#Elasticsearch에 질의하는 코드를 묶어논 함수입니다.
def get_video_documents(keyword,gte,sort_value,video_counts):
    if sort_value is not None:
        video_documents = (
            VideoDocument
                .search()
                .filter('match', videokeywordnews__keyword=keyword)
                .filter('range', upload_time={'gte': gte, 'lt': "now"})
                .sort({sort_value: "desc"})[:video_counts]
        )
    else:
        video_documents = (
            VideoDocument
                .search()
                .filter('match', videokeywordnews__keyword=keyword)
                .filter('range', upload_time={'gte': gte, 'lt': "now"})
        )
    return video_documents


#직렬화된 word_map data에 색깔을 추가하는 함수입니다.
def add_color_to_keyword(word_map_keywords):
    for item_index in range(len(word_map_keywords)):
        if item_index == 0:
            word_map_keywords[item_index].update({'color': '#f9bf69'})
        elif item_index == 1:
            word_map_keywords[item_index].update({'color': '#f65a5a'})
        elif item_index == 2:
            word_map_keywords[item_index].update({'color': '#508ddc'})
        elif item_index == 3:
            word_map_keywords[item_index].update({'color': '#f9bf69'})
        elif item_index == 4:
            word_map_keywords[item_index].update({'color': '#f65a5a'})
        else:
            word_map_keywords[item_index].update({'color': '#508ddc'})
    return word_map_keywords


#많은 키워드들 중 counter 모듈을 이용해 가장 많이 등장하는 키워드 6개를 추출하는 함수입니다.
def word_map_keyword_counter(video_documents):
    word_map_keyword = []
    for video_document in video_documents:
        video_key_tmp = [video_keyword.keyword for video_keyword in video_document.videokeywordnews]
        word_map_keyword.append(video_key_tmp)
    word_map_keyword = list(itertools.chain(*word_map_keyword))
    counter = collections.Counter(word_map_keyword)
    word_map_keyword = dict(counter.most_common(n=6))
    word_map_keyword = [{"name": key, "value": word_map_keyword[key]} for key in word_map_keyword.keys()]

    word_map_keyword = [Keyword(keyword=keyword) for keyword in word_map_keyword]
    return word_map_keyword


#영상화 키워드 가공 및 직렬화 전체 프로세스를 담당하는 함수입니다.
def channel_imaging_keyword(keyword):
    #데이터 요청 및 가공
    imaging_transition_list = get_imaging_transition(keyword)
    imaging_video_sum = get_video_sum(imaging_transition_list)
    imaging_video_avg = get_video_avg(imaging_video_sum, len(imaging_transition_list))
    video_documents = get_video_documents(keyword=keyword, gte='now-14d/d', sort_value='upload_time', video_counts=500)
    word_map_keyword = word_map_keyword_counter(video_documents)
    #데이터 직렬화
    serialized_word_map_keyword = KeywordCountSerializer(word_map_keyword, many=True)
    top_view_video_documents=get_video_documents(keyword=keyword,gte='now-7d/d',sort_value='views',video_counts=5)
    serialized_views_top5_video = VideoSerializer(top_view_video_documents, many=True)
    #직렬화된 데이터 색깔추가
    word_map_keywords_with_color = add_color_to_keyword(serialized_word_map_keyword.data)
    return Response({"type": "영상", "keyword": [
        {"name": keyword, "popular": imaging_video_avg, "wordmap": {"name": keyword, 'color': '#666',
                                                             "children": word_map_keywords_with_color},
         "lines": {'type': "영상화 추이", 'data': imaging_transition_list},
         "video": {"type": "analysis",
                   "data": serialized_views_top5_video.data}}]})


#Elasticsearch에 해당 키워드가 영상화 된 최근 7일치 데이터를 일자별로 질의 후 가공, 리스트로 반환하는 함수입니다.
def get_popular_transition(keyword):
    #Elasticsearch query입니다.
    query_popular_transition = (
        VideoDocument
            .search()
            .filter('match', videokeywordnews__keyword=keyword)
            .filter('range', upload_time={'gte': 'now-8d/d', 'lt': "now"})
    )
    # aggregation bucket 메소드를 이용하여 날짜별로 데이터를 집합(인기도 평균으로)합니다.
    query_popular_transition.aggs.bucket('mola', A('date_histogram', field='upload_time', calendar_interval='1d')) \
        .metric('popularity_per_day', A('avg', field='popularity'))
    response = query_popular_transition.execute()
    popular_transition_list = []
    for tag in response.aggregations.mola.buckets:
        if tag.popularity_per_day.value is not None:
            popular_transition_list.append(
                {'date': tag.key_as_string[:10], 'value': tag.popularity_per_day.value * 100})
        else:
            popular_transition_list.append({'date': tag.key_as_string[:10], 'value': 0})

    return popular_transition_list


#인기 키워드 가공 및 직렬화 전체 프로세스를 담당하는 함수입니다.
def channel_popular_keyword(keyword):
    #데이터 요청 및 가공
    popular_transition_list = get_popular_transition(keyword)
    popular_video_sum = get_video_sum(popular_transition_list)
    popular_video_avg = get_video_avg(popular_video_sum, len(popular_transition_list))
    video_documents = get_video_documents(keyword=keyword, gte='now-7d/d', sort_value='upload_time', video_counts=500)
    word_map_keyword = word_map_keyword_counter(video_documents)
    #데이터 직렬화
    top5_popular_video_documents = get_video_documents(keyword=keyword, gte='now-7d/d', sort_value='popularity', video_counts=5)
    serialized_word_map_keyword = KeywordCountSerializer(word_map_keyword, many=True)
    serialized_top5_popular_video = VideoSerializer(top5_popular_video_documents, many=True)
    #직렬화된 데이터에 색깔 추가
    word_map_keywords_with_color = add_color_to_keyword(serialized_word_map_keyword.data)
    return Response({"type": "인기", "keyword": [{"name": keyword, "popular": popular_video_avg,
                                                "wordmap": {"name": keyword, 'color': '#666',
                                                            "children": word_map_keywords_with_color},
                                                "lines": {"type": "인기도 추이", "data": popular_transition_list},
                                                "video": {"type": "analysis",
                                                          "data": serialized_top5_popular_video.data}}]})


#가장 인기가 많았던 10개의 키워드를 추출,가공 및 직렬화하는 함수입니다.
def get_popular_top10_keyword():
    #Elasticsearch query입니다.
    popular_video = (
        VideoDocument
            .search()
            .filter('range', popularity={'lte': 50})
            .exclude('terms',
                     channel_idx=[2409, 2438, 2544, 2388, 2465, 2412, 2386, 1063, 2417, 2488, 2476, 2357, 2425, 2416,
                                  2454, 2461, 2399, 1069, 2394, 2422])
            .filter('range', upload_time={'gte': 'now-7d/d', 'lt': "now"})
            .sort({"popularity": "desc"})[:300]
    )

    #counter 모듈을 이용해 top10 인기 키워드 구하는 과정
    popular_keywords = []
    for video in popular_video:
        keyword = [keywords.keyword for keywords in video.videokeywordnews if
                   keywords.keyword not in ["yt:cc=on", "lol", "리그오브레전드", "외국반응", "일본반응", "쇼미9", "롤 매드무비", "롤 하이라이트",
                                            "league of legends", "영화리뷰", "뉴스", "게임", "해외반응", "만화", "애니", "모바일게임", "한국",
                                            "일본"]]
        popular_keywords.append(keyword)
    top10_popular_keywords = list(itertools.chain(*popular_keywords))
    counter = collections.Counter(top10_popular_keywords)
    top10_popular_keywords = dict(counter.most_common(n=10))
    top10_popular_keywords = [{"name": key, "value": top10_popular_keywords[key]} for key in
                              top10_popular_keywords.keys()]
    top10_popular_keywords = [Keyword(keyword=keyword) for keyword in top10_popular_keywords]
    
    #데이터 직렬화
    serialized_popular_top10_keyword = KeywordCountSerializer(top10_popular_keywords, many=True)
    return {"type": "인기", "keyword": serialized_popular_top10_keyword.data}


#가장 영상화가 많았던 10개의 키워드를 추출,가공 및 직렬화하는 함수입니다.
def get_imaging_top10_keyword():
    #Elasticsearch query입니다.
    imaging_video = (
        VideoDocument
            .search()
            .filter('range', popularity={'gte': 0.3})
            .filter('term', crawled=True)
            .exclude('terms',
                     channel_idx=[2409, 2438, 2544, 2388, 2465, 2412, 2386, 1063, 2417, 2488, 2476, 2357, 2425, 2416,
                                  2454, 2461, 2399, 1069, 2394, 2422, 484, 2291, 2567, 2565, 2572, 2464, 2592, 2564,
                                  2570, 2577, 2508, 2575, 2568, 2418, 2527, 2539, 2436, 2589, 2571, 2574, 2169, 2596,
                                  2293, 739, 2289, 701, 736, 1877, 2463, 1561, 605, 2157, 497, 1318, 493, 566, 568, 766,
                                  707, 535, 756, 10307])
            .filter('range', upload_time={'gte': 'now-7d/d', 'lt': "now"})
            .sort({"upload_time": "desc"})[:700]
    )

    #counter 모듈을 이용해 top10 영상화 키워드 구하는 과정
    top10_imaging_keywords = []
    for video in imaging_video:
        keyword = [keywords.keyword for keywords in video.videokeywordnews if
                   keywords.keyword not in ["lol", "yt:cc=on", '게임', '모바일게임', '축구', '브이로그', '애니메이션', "주식", "뉴스", "강의",
                                            "미국", "한국", "일본", "리그오브레전드", "LOL"]]
        top10_imaging_keywords.append(keyword)
    top10_imaging_keywords = list(itertools.chain(*top10_imaging_keywords))
    counter = collections.Counter(top10_imaging_keywords)
    top10_imaging_keywords = dict(counter.most_common(n=10))

    top10_imaging_keywords = [{"name": key, "value": top10_imaging_keywords[key]} for key in top10_imaging_keywords.keys()]
    top10_imaging_keywords = [Keyword(keyword=keyword) for keyword in top10_imaging_keywords]
    
    #데이터 직렬화
    serialized_imaging_top10_keyword = KeywordCountSerializer(top10_imaging_keywords, many=True)
    return {"type": "영상화", "keyword": serialized_imaging_top10_keyword.data}