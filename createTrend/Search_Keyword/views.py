from django.shortcuts import render
from rest_framework import viewsets  
from rest_framework.decorators import api_view
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework.pagination import PageNumberPagination
from django.db.models import Max ,Count, Sum, OuterRef, Subquery
from Search_Keyword.serializers import ChannelListSerializer, VideoKeywordSerializer, TopVideoSerializer\
    ,RecentVideoSerializer, KeywordCountSerializer
from .models import Channel, VideoKeywordNew, Video, VideoViews,ChannelSubscriber
from rest_framework.response import Response
import datetime, itertools, collections
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# from Search_Keyword.serializers import topComment
# Create your views here.
# class topCommentViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
param_search_hint = openapi.Parameter(
        'search',
        openapi.IN_QUERY,
        description='검색하고 싶은 키워드를 입력하세요.',
        type=openapi.TYPE_STRING
    )

@swagger_auto_schema(method='get',manual_parameters=[param_search_hint])
@api_view(['GET'])
def keyword(request):
    '''
    키워드 검색 API
    ---
    검색한 키워드와 관련된 최근 영상과, 인기있는 영상, 관련 키워드 워드맵 정보 등을 제공하는 api입니다.
    '''
    if request.method == 'GET':
        search=request.query_params.get('search')
        if search:
            start=timezone.now()-datetime.timedelta(days=14)
            start=start.strftime("%Y-%m-%d")
            end=timezone.now().strftime("%Y-%m-%d")
            # topVideo =Video.objects.all()\
            #     .filter(videokeywordnew__keyword=search, upload_time__range=(start,end))\
            #     .order_by('-videoviews__views')[:10]
            recentVideo = Video.objects.all()\
                .filter(videokeywordnew__keyword__contains=search, upload_time__range=(start,end))\
                .annotate(recent_video_made_at=Max('upload_time'))
                # .order_by('-upload_time')[:5]  
            recentVideo=Video.objects.filter(
                upload_time__in=[v.recent_video_made_at for v in recentVideo]
                ).order_by('-upload_time')[:5]
            videos = Video.objects.filter(videokeywordnew__keyword__contains=search, upload_time__range=(start,end))\
                .annotate(hottest_video_made_at=Max('videoviews__check_time')) 
            hottest_videos = VideoViews.objects.filter(
                check_time__in=[v.hottest_video_made_at for v in videos]
                ).order_by('-views')[:5]
            # recentVideo = 
            topVideo=[]
            for hv in hottest_videos:
                topVideo.append(hv.video_idx)
            # videos = channel.video.all().prefetch_related('videokeyword')
            keywordVideo=Video.objects.all()\
                .filter(videokeywordnew__keyword__contains=search, upload_time__range=(start,end))\
                .order_by('-upload_time')[:1000].prefetch_related('videokeywordnew')  
            keywords=[]

            for video in keywordVideo:
                keyword=[videokeyword.keyword for videokeyword in video.videokeywordnew.all()]
                keywords.append(keyword)
            keywords=list(itertools.chain(*keywords))
            while search in keywords:
                keywords.remove(search)
            counter=collections.Counter(keywords)
            keywords=dict(counter.most_common(n=7))
            keywords=[{"name":key,"value":keywords[key]} for key in keywords.keys()]
            class Keyword(object):
                def __init__(self,keyword):
                    self.name = keyword['name']
                    self.value=keyword['value']
            keywords=[Keyword(keyword=keyword) for keyword in keywords]

            imagingTransition = list(Video.objects.all()\
                .filter(videokeywordnew__keyword__contains=search, upload_time__range=(start,end))\
                .extra(select={'date': "TO_CHAR(upload_time, 'YYYY-MM-DD')"}).values('date') \
                .annotate(value=Count('idx')))
            popularTranstitionViews = list(Video.objects.all()\
                .filter(videokeywordnew__keyword__contains=search, upload_time__range=(start,end))\
                .extra(select={'date': "TO_CHAR(upload_time, 'YYYY-MM-DD')"}).values('date') \
                .annotate(value=Sum('videoviews__views')))
            popularTranstitionSubscriber = Video.objects.prefetch_related('channel_idx','channel_idx__channelsubscriber')\
                .filter(videokeywordnew__keyword__contains=search, upload_time__range=(start,end))\
                .extra(select={'date': "TO_CHAR(upload_time, 'YYYY-MM-DD')"})
            ChannelSubscriberQuery=ChannelSubscriber.objects.all()
            subscribers={}
            for video in popularTranstitionSubscriber:
                # print(video)
                subscriber = video.channel_idx.channelsubscriber.first().subscriber_num
                # print(subscriber_num)
                if video.date in subscribers:
                    subscribers[video.date]+=int(subscriber)
                else:
                    subscribers.update({video.date:int(subscriber)})
            subdict={}
            for i in range(len(popularTranstitionViews)):
                subdict[popularTranstitionViews[i]['date']]=popularTranstitionViews[i]['value']/subscribers[popularTranstitionViews[i]['date']]*100
            subscribers=[]
            for key in subdict.keys():
                subscribers.append({"date":key,"value":subdict[key]})
                # .annotate(value=Sum()))
            #channel_subscriber__check_time=date&&channel_subscriber__channel_idx=channel_idx__idx
            # print(popularTranstitionSubscriber)
            popularTopKeyword = Video.objects.all()\
                .filter(videokeywordnew__keyword__contains=search, upload_time__range=(start,end))\
                .order_by('-popularity').prefetch_related('videokeywordnew')[:100]
            topPopularKeywords=[]
            for popularKeyword in popularTopKeyword.iterator():
                # print(popularKeyword.videokeywordnew.all())
                keyword = [popkeywords.keyword for popkeywords in popularKeyword.videokeywordnew.all()]
                topPopularKeywords.append(keyword)
            topPopularKeywords=list(itertools.chain(*topPopularKeywords))
            counter=collections.Counter(topPopularKeywords)
            topPopularKeywords=dict(counter.most_common(n=11))
            try:
                del(topPopularKeywords[search])
            except:
                pass
            topPopularKeywords=[{"name":key,"value":topPopularKeywords[key]} for key in topPopularKeywords.keys()]
            topPopularKeywords=[Keyword(keyword=keyword) for keyword in topPopularKeywords]
            imagingTransitionKeyword = list(Video.objects.prefetch_related('videokeywordnew')\
                .filter(videokeywordnew__keyword__contains=search, upload_time__range=(start,end)))
            
            topImagingKeywords=[]
            for imagingkeywordvideo in imagingTransitionKeyword:
                keyword = [imagingkeywords.keyword for imagingkeywords in imagingkeywordvideo.videokeywordnew.all()]
                topImagingKeywords.append(keyword)
            topImagingKeywords=list(itertools.chain(*topImagingKeywords))
            counter=collections.Counter(topImagingKeywords)
            topImagingKeywords=dict(counter.most_common(n=11))
            try:   
                del(topImagingKeywords[search])
            except:
                pass
            topImagingKeywords=[{"name":key,"value":topImagingKeywords[key]} for key in topImagingKeywords.keys()]
            topImagingKeywords=[Keyword(keyword=keyword) for keyword in topImagingKeywords]
            
            topImagingKeywordCountSerializer=KeywordCountSerializer(topImagingKeywords,many=True)
            topkeywordCountSerializer=KeywordCountSerializer(topPopularKeywords,many=True)
            keywordCountSerializer=KeywordCountSerializer(keywords,many=True)
            print('e')   
            topVideoSerializer = TopVideoSerializer(topVideo,many=True)
            recentVideoSerializer = RecentVideoSerializer(recentVideo,many=True)
            return Response({'video':[{"type":"analysis","data":topVideoSerializer.data},\
                {"type":"aside","data":recentVideoSerializer.data}], 'wordmap':{'name':search,'children':keywordCountSerializer.data}\
                    ,"lines":[{"type":"영상화 추이","data":imagingTransition},{"type":"인기도 추이","data":subscribers}]\
                    ,"keyword":[{"type":"인기 키워드","keyword":topkeywordCountSerializer.data},{"type":"영상화 키워드","keyword":topImagingKeywordCountSerializer.data}]}) 
        else:
            paginator = PageNumberPagination()
            paginator.page_size = 10
            queryset = VideoKeywordNew.objects.all()
            result_page = paginator.paginate_queryset(queryset, request)
            serializer = VideoKeywordSerializer(result_page,many=True)
            return paginator.get_paginated_response(serializer.data) 

      
