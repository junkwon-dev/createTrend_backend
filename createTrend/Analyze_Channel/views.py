from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import F, Count, Sum, Max
import datetime, itertools, collections
from .models import Channel, VideoKeywordNew, Video, ChannelSubscriber, VideoViews
from .serializers import VideoKeywordSerializer, KeywordCountSerializer,VideoSerializer
# Create your views here.

def imagingIncreaseRate(keyword):
    #전주
    start=timezone.now()-datetime.timedelta(days=14)
    start=start.strftime("%Y-%m-%d")
    end=(timezone.now()-datetime.timedelta(days=7)).strftime("%Y-%m-%d")
    imagingTransition = list(Video.objects.all()\
        .filter(videokeywordnew__keyword__contains=keyword, upload_time__range=(start,end))\
        .extra(select={'date': "TO_CHAR(upload_time, 'YYYY-MM-DD')"}).values('date') \
        .annotate(value=Count('idx')))
    imagingVideoSum=0
    for imagingvideo in imagingTransition:
        imagingVideoSum+=imagingvideo['value']
    try:
        lastWeekAvgImaging=imagingVideoSum/len(imagingTransition)
    except:
        lastWeekAvgImaging=0
    #이번주
    start=timezone.now()-datetime.timedelta(days=7)
    start=start.strftime("%Y-%m-%d")
    end=timezone.now().strftime("%Y-%m-%d")
    imagingTransition = list(Video.objects.all()\
        .filter(videokeywordnew__keyword__contains=keyword, upload_time__range=(start,end))\
        .extra(select={'date': "TO_CHAR(upload_time, 'YYYY-MM-DD')"}).values('date') \
        .annotate(value=Count('idx')))
    imagingVideoSum=0
    for imagingvideo in imagingTransition:
        imagingVideoSum+=imagingvideo['value']
    try:
        thisWeekAvgImaging=imagingVideoSum/len(imagingTransition)
    except:
        thisWeekAvgImaging=0
    try:
        weekAvgIncrease = (thisWeekAvgImaging - lastWeekAvgImaging)/lastWeekAvgImaging * 100
    except:
        weekAvgIncrease=0
    
    #전날
    start=timezone.now()-datetime.timedelta(days=2)
    start=start.strftime("%Y-%m-%d")
    end=(timezone.now()-datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    imagingTransition = list(Video.objects.all()\
        .filter(videokeywordnew__keyword__contains=keyword, upload_time__range=(start,end))\
        .extra(select={'date': "TO_CHAR(upload_time, 'YYYY-MM-DD')"}).values('date') \
        .annotate(value=Count('idx')))
    imagingVideoSum=0
    for imagingvideo in imagingTransition:
        imagingVideoSum+=imagingvideo['value']
    try:
        lastDayAvgImaging=imagingVideoSum/len(imagingTransition)
    except:
        lastDayAvgImaging=0
    #오늘
    start=timezone.now()-datetime.timedelta(days=1)
    start=start.strftime("%Y-%m-%d")
    end=timezone.now().strftime("%Y-%m-%d")
    imagingTransition = list(Video.objects.all()\
        .filter(videokeywordnew__keyword__contains=keyword, upload_time__range=(start,end))\
        .extra(select={'date': "TO_CHAR(upload_time, 'YYYY-MM-DD')"}).values('date') \
        .annotate(value=Count('idx')))
    imagingVideoSum=0
    for imagingvideo in imagingTransition:
        imagingVideoSum+=imagingvideo['value']
    try:
        thisDayAvgImaging=imagingVideoSum/len(imagingTransition)
    except:
        thisDayAvgImaging=0
    try:
        dayAvgIncrease = (thisDayAvgImaging - lastDayAvgImaging)/lastDayAvgImaging * 100
    except:
        dayAvgIncrease=0
    return weekAvgIncrease,dayAvgIncrease


@api_view(['GET'])
def keyword_data(request):
    search=request.query_params.get('search')
    keyword=request.query_params.get('keyword')
    if (search == '영상화' and keyword):
        # weekAvgIncrease,dayAvgIncrease=imagingIncreaseRate(keyword)
        start=timezone.now()-datetime.timedelta(days=14)
        start=start.strftime("%Y-%m-%d")
        end=timezone.now().strftime("%Y-%m-%d")
        imagingTransition = list(Video.objects.all()\
            .filter(videokeywordnew__keyword__contains=keyword, upload_time__range=(start,end))\
            .extra(select={'date': "TO_CHAR(upload_time, 'YYYY-MM-DD')"}).values('date') \
            .annotate(value=Count('idx')))
        imagingVideoSum=0
        for imagingvideo in imagingTransition:
            imagingVideoSum+=imagingvideo['value']
        avgImaging=imagingVideoSum/len(imagingTransition)
        keywordVideo=Video.objects.all()\
            .filter(videokeywordnew__keyword__contains=keyword, upload_time__range=(start,end))\
            .order_by('-upload_time')[:1000].prefetch_related('videokeywordnew')  
        keywords=[]
        for video in keywordVideo:
            videokeytmp=[videokeyword.keyword for videokeyword in video.videokeywordnew.all()]
            keywords.append(videokeytmp)
        keywords=list(itertools.chain(*keywords))
        while keyword in keywords:
            keywords.remove(keyword)
        counter=collections.Counter(keywords)
        keywords=dict(counter.most_common(n=7))
        keywords=[{"name":key,"value":keywords[key]} for key in keywords.keys()]
        class Keyword(object):
            def __init__(self,keyword):
                self.name = keyword['name']
                self.value=keyword['value']
        keywords=[Keyword(keyword=keyword) for keyword in keywords]
        keywordCountSerializer=KeywordCountSerializer(keywords,many=True)
        videos = Video.objects.filter(videokeywordnew__keyword__contains=keyword, upload_time__range=(start,end))\
            .annotate(hottest_video_made_at=Max('videoviews__check_time')) 
        
        hottest_videos = VideoViews.objects.filter(
            check_time__in=[v.hottest_video_made_at for v in videos]
            ).order_by('-views')[:5]
        topViewVideo=[]
        for hv in hottest_videos:
            topViewVideo.append(hv.video_idx)     
        topViewVideoSerializer=VideoSerializer(topViewVideo,many=True)
        # return Response([imagingTransition,keywordCountSerializer.data])
        return Response({"type":"영상","keyword":[{"name":keyword,"popular":avgImaging,"wordmap":keywordCountSerializer.data,"lines":imagingTransition,"video":topViewVideoSerializer.data}]})
    elif (search == '인기' and keyword):
        #전주
        # start=timezone.now()-datetime.timedelta(days=14)
        # start=start.strftime("%Y-%m-%d")
        # end=(timezone.now()-datetime.timedelta(days=7)).strftime("%Y-%m-%d")
        # popularTransitionViews = list(Video.objects.all()\
        #     .filter(videokeywordnew__keyword__contains=keyword, upload_time__range=(start,end))\
        #     .extra(select={'date': "TO_CHAR(upload_time, 'YYYY-MM-DD')"}).values('date') \
        #     .annotate(value=Sum('videoviews__views')))
        # popularTransitionSubscriber = list(Video.objects.all()\
        #     .filter(videokeywordnew__keyword__contains=keyword, upload_time__range=(start,end))\
        #     .extra(select={'date': "TO_CHAR(upload_time, 'YYYY-MM-DD')"}).values('date','channel_idx'))
        # subscribers={}
        # for video in popularTransitionSubscriber:
        #     subscriber = ChannelSubscriber.objects.filter(channel_idx=video['channel_idx'])
        #     subscriber_num=subscriber[0].subscriber_num
        #     if video['date'] in subscribers:
        #         subscribers[video['date']]=int(subscribers[video['date']])+int(subscriber_num)
        #     else:
        #         subscribers[video['date']]=int(subscriber_num)
        # popularDict={}
        # popularDictSum=0
        # for i in range(len(popularTransitionViews)):
        #     popularDict[popularTransitionViews[i]['date']]=popularTransitionViews[i]['value']/subscribers[popularTransitionViews[i]['date']]*100
        #     popularDictSum+=popularDict[popularTransitionViews[i]['date']]
        # lastweekAvgPupularDict=popularDictSum/len(popularTransitionViews)
        # #이번주평균
        # start=timezone.now()-datetime.timedelta(days=7)
        # start=start.strftime("%Y-%m-%d")
        # end=timezone.now().strftime("%Y-%m-%d")
        # popularTransitionViews = list(Video.objects.all()\
        #     .filter(videokeywordnew__keyword__contains=keyword, upload_time__range=(start,end))\
        #     .extra(select={'date': "TO_CHAR(upload_time, 'YYYY-MM-DD')"}).values('date') \
        #     .annotate(value=Sum('videoviews__views')))
        # popularTransitionSubscriber = list(Video.objects.all()\
        #     .filter(videokeywordnew__keyword__contains=keyword, upload_time__range=(start,end))\
        #     .extra(select={'date': "TO_CHAR(upload_time, 'YYYY-MM-DD')"}).values('date','channel_idx'))
        # subscribers={}
        # for video in popularTransitionSubscriber:
        #     subscriber = ChannelSubscriber.objects.filter(channel_idx=video['channel_idx'])
        #     subscriber_num=subscriber[0].subscriber_num
        #     if video['date'] in subscribers:
        #         subscribers[video['date']]=int(subscribers[video['date']])+int(subscriber_num)
        #     else:
        #         subscribers[video['date']]=int(subscriber_num)
        # popularDict={}
        # popularDictSum=0
        # for i in range(len(popularTransitionViews)):
        #     popularDict[popularTransitionViews[i]['date']]=popularTransitionViews[i]['value']/subscribers[popularTransitionViews[i]['date']]*100
        #     popularDictSum+=popularDict[popularTransitionViews[i]['date']]
        # try:
        #     thisweekAvgPupularDict=popularDictSum/len(popularTransitionViews)
        # except:
        #     thisweekAvgPupularDict=0
        # #증감률
        # try:
        #     increaseRateWeek=(lastweekAvgPupularDict-thisweekAvgPupularDict)/lastweekAvgPupularDict*100
        # except:
        #     increaseRateWeek=0
        # #전날
        # start=timezone.now()-datetime.timedelta(days=2)
        # start=start.strftime("%Y-%m-%d")
        # end=(timezone.now()-datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        # popularTransitionViews = list(Video.objects.all()\
        #     .filter(videokeywordnew__keyword__contains=keyword, upload_time__range=(start,end))\
        #     .extra(select={'date': "TO_CHAR(upload_time, 'YYYY-MM-DD')"}).values('date') \
        #     .annotate(value=Sum('videoviews__views')))
        # popularTransitionSubscriber = list(Video.objects.all()\
        #     .filter(videokeywordnew__keyword__contains=keyword, upload_time__range=(start,end))\
        #     .extra(select={'date': "TO_CHAR(upload_time, 'YYYY-MM-DD')"}).values('date','channel_idx'))
        # subscribers={}
        # for video in popularTransitionSubscriber:
        #     subscriber = ChannelSubscriber.objects.filter(channel_idx=video['channel_idx'])
        #     subscriber_num=subscriber[0].subscriber_num
        #     if video['date'] in subscribers:
        #         subscribers[video['date']]=int(subscribers[video['date']])+int(subscriber_num)
        #     else:
        #         subscribers[video['date']]=int(subscriber_num)
        # popularDict={}
        # popularDictSum=0
        # for i in range(len(popularTransitionViews)):
        #     popularDict[popularTransitionViews[i]['date']]=popularTransitionViews[i]['value']/subscribers[popularTransitionViews[i]['date']]*100
        #     popularDictSum+=popularDict[popularTransitionViews[i]['date']]
        # try:
        #     lastdayAvgPupularDict=popularDictSum/len(popularTransitionViews)
        # except:
        #     lastdayAvgPupularDict=0
        # #오늘평균
        # start=timezone.now()-datetime.timedelta(days=1)
        # start=start.strftime("%Y-%m-%d")
        # end=timezone.now().strftime("%Y-%m-%d")
        # popularTransitionViews = list(Video.objects.all()\
        #     .filter(videokeywordnew__keyword__contains=keyword, upload_time__range=(start,end))\
        #     .extra(select={'date': "TO_CHAR(upload_time, 'YYYY-MM-DD')"}).values('date') \
        #     .annotate(value=Sum('videoviews__views')))
        # popularTransitionSubscriber = list(Video.objects.all()\
        #     .filter(videokeywordnew__keyword__contains=keyword, upload_time__range=(start,end))\
        #     .extra(select={'date': "TO_CHAR(upload_time, 'YYYY-MM-DD')"}).values('date','channel_idx'))
        # subscribers={}
        # for video in popularTransitionSubscriber:
        #     subscriber = ChannelSubscriber.objects.filter(channel_idx=video['channel_idx'])
        #     subscriber_num=subscriber[0].subscriber_num
        #     if video['date'] in subscribers:
        #         subscribers[video['date']]=int(subscribers[video['date']])+int(subscriber_num)
        #     else:
        #         subscribers[video['date']]=int(subscriber_num)
        # popularDict={}
        # popularDictSum=0
        # for i in range(len(popularTransitionViews)):
        #     popularDict[popularTransitionViews[i]['date']]=popularTransitionViews[i]['value']/subscribers[popularTransitionViews[i]['date']]*100
        #     popularDictSum+=popularDict[popularTransitionViews[i]['date']]
        # try:
        #     todayAvgPupularDict=popularDictSum/len(popularTransitionViews)
        # except:
        #     todayAvgPupularDict=0
        # #증감률
        # try:
        #     increaseRateDay=(lastdayAvgPupularDict-todayAvgPupularDict)/lastdayAvgPupularDict*100
        # except:
        #     increaseRateDay=0
        
        start=timezone.now()-datetime.timedelta(days=14)
        start=start.strftime("%Y-%m-%d")
        end=timezone.now().strftime("%Y-%m-%d")
        popularTransitionViews = list(Video.objects.all()\
            .filter(videokeywordnew__keyword__contains=keyword, upload_time__range=(start,end))\
            .extra(select={'date': "TO_CHAR(upload_time, 'YYYY-MM-DD')"}).values('date') \
            .annotate(value=Sum('videoviews__views')))
        popularTransitionSubscriber = list(Video.objects.all()\
            .filter(videokeywordnew__keyword__contains=keyword, upload_time__range=(start,end))\
            .extra(select={'date': "TO_CHAR(upload_time, 'YYYY-MM-DD')"}).values('date','channel_idx'))
        subscribers={}
        for video in popularTransitionSubscriber:
            subscriber = ChannelSubscriber.objects.filter(channel_idx=video['channel_idx'])
            subscriber_num=subscriber[0].subscriber_num
            if video['date'] in subscribers:
                subscribers[video['date']]=int(subscribers[video['date']])+int(subscriber_num)
            else:
                subscribers[video['date']]=int(subscriber_num)
        popularDict={}
        popularDictSum=0
        for i in range(len(popularTransitionViews)):
            popularDict[popularTransitionViews[i]['date']]=popularTransitionViews[i]['value']/subscribers[popularTransitionViews[i]['date']]*100
            popularDictSum+=popularDict[popularTransitionViews[i]['date']]
        avgPupularDict=popularDictSum/len(popularTransitionViews)
        
        popularTransition=[]
        for subdictKey in popularDict.keys():
            popularTransition.append({"date":subdictKey,"value":popularDict[subdictKey]})
        keywordVideo=Video.objects.all()\
            .filter(videokeywordnew__keyword__contains=keyword, upload_time__range=(start,end))\
            .order_by('-upload_time')[:1000].prefetch_related('videokeywordnew')  
        keywords=[]
        for video in keywordVideo:
            videokeytmp=[videokeyword.keyword for videokeyword in video.videokeywordnew.all()]
            keywords.append(videokeytmp)
        keywords=list(itertools.chain(*keywords))
        while keyword in keywords:
            keywords.remove(keyword)
        counter=collections.Counter(keywords)
        keywords=dict(counter.most_common(n=7))
        keywords=[{"name":key,"value":keywords[key]} for key in keywords.keys()]
        class Keyword(object):
            def __init__(self,keyword):
                self.name = keyword['name']
                self.value=keyword['value']
        keywords=[Keyword(keyword=keyword) for keyword in keywords]
        
        popularVideo=Video.objects.all()\
            .filter(videokeywordnew__keyword__contains=keyword, upload_time__range=(start,end))\
            .order_by(F('popularity').desc(nulls_last=True))[:5]        
        popularVideoSerializer=VideoSerializer(popularVideo,many=True)
        
        keywordCountSerializer=KeywordCountSerializer(keywords,many=True)
        
        # return Response([popularDict,keywordCountSerializer.data])
        return Response({"type":"인기","keyword":[{"name":keyword,"popular":avgPupularDict,"wordmap":keywordCountSerializer.data,"lines":popularTransition,"video":popularVideoSerializer.data}]})

    return Response("")
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

    
        
    
    topImagingKeywordCountSerializer=KeywordCountSerializer(topImagingKeywords,many=True)
    topkeywordCountSerializer=KeywordCountSerializer(topPopularKeywords,many=True)
    return Response([{"type":"인기","data":topkeywordCountSerializer.data},{"type":"영상화","data":topImagingKeywordCountSerializer.data}])