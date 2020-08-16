from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import F, Count, Sum
import datetime, itertools, collections
from .models import Channel, VideoKeywordNew, Video, ChannelSubscriber
from .serializers import VideoKeywordSerializer, KeywordCountSerializer
# Create your views here.
@api_view(['GET'])
def analyze_channel(request):
    search=None
    start=timezone.now()-datetime.timedelta(days=14)
    start=start.strftime("%Y-%m-%d")
    end=timezone.now().strftime("%Y-%m-%d")
    class Keyword(object):
        def __init__(self,keyword):
            self.name = keyword['name']
            self.value=keyword['value']
    popularTopKeyword = list(Video.objects.all()\
        .filter(upload_time__range=(start,end))\
        .order_by(F('popularity').desc(nulls_last=True)).prefetch_related('videokeywordnew')[:1000])
    topPopularKeywords=[]
    for popularKeyword in popularTopKeyword:
        # print(VideoKeywordNew.objects.filter(video_idx=popularKeyword.idx))
        keyword = [keywords.keyword for keywords in popularKeyword.videokeywordnew.all()]
        topPopularKeywords.append(keyword)
    topPopularKeywords=list(itertools.chain(*topPopularKeywords))
    counter=collections.Counter(topPopularKeywords)
    topPopularKeywords=dict(counter.most_common(n=10))
    topPopularKeywords=[{"name":key,"value":topPopularKeywords[key]} for key in topPopularKeywords.keys()]
    topPopularKeywords=[Keyword(keyword=keyword) for keyword in topPopularKeywords]
    #영상화 키워드
    start=timezone.now()-datetime.timedelta(days=7)
    start=start.strftime("%Y-%m-%d")
    end=timezone.now().strftime("%Y-%m-%d")
    imagingTransitionKeyword = list(Video.objects.all()\
        .filter(upload_time__range=(start,end)).prefetch_related('videokeywordnew'))
    
    topImagingKeywords=[]
    for imagingkeywordvideo in imagingTransitionKeyword:
        keyword = [keywords.keyword for keywords in imagingkeywordvideo.videokeywordnew.all()]
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
    print(topImagingKeywords)
    for data in topImagingKeywords:
        imagingTransition = list(Video.objects.all()\
            .filter(videokeywordnew__keyword__contains=data.name, upload_time__range=(start,end))\
            .extra(select={'date': "TO_CHAR(upload_time, 'YYYY-MM-DD')"}).values('date') \
            .annotate(value=Count('idx')))
    for data in topPopularKeywords:
        popularTranstitionViews = list(Video.objects.all()\
            .filter(videokeywordnew__keyword__contains=data.name, upload_time__range=(start,end))\
            .extra(select={'date': "TO_CHAR(upload_time, 'YYYY-MM-DD')"}).values('date') \
            .annotate(value=Sum('videoviews__views')))
        popularTranstitionSubscriber = list(Video.objects.all()\
            .filter(videokeywordnew__keyword__contains=data.name, upload_time__range=(start,end))\
            .extra(select={'date': "TO_CHAR(upload_time, 'YYYY-MM-DD')"}).values('date','channel_idx'))
        subscribers={}
        for video in popularTranstitionSubscriber:
            res = (datetime.datetime.strptime(video['date'], '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
            subscriber = ChannelSubscriber.objects.filter(channel_idx=video['channel_idx'])
            subscriber_num=subscriber[0].subscriber_num
            if video['date'] in subscribers:
                subscribers[video['date']]=int(subscribers[video['date']])+int(subscriber_num)
            else:
                subscribers[video['date']]=int(subscriber_num)
        subdict={}
        for i in range(len(popularTranstitionViews)):
            subdict[popularTranstitionViews[i]['date']]=popularTranstitionViews[i]['value']/subscribers[popularTranstitionViews[i]['date']]*100
        subscribers=[]
        for key in subdict.keys():
            subscribers.append({"date":key,"value":subdict[key]})
    
    
    topImagingKeywordCountSerializer=KeywordCountSerializer(topImagingKeywords,many=True)
    topkeywordCountSerializer=KeywordCountSerializer(topPopularKeywords,many=True)
    return Response([topkeywordCountSerializer.data,topImagingKeywordCountSerializer.data],{"lines":[{"type":"영상화 키워드","data":imagingTransition},{"type":"인기 키워드","data":subscribers}]})