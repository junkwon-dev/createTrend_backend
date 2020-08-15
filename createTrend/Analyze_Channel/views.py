from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import F
import datetime, itertools, collections
from .models import Channel, VideoKeywordNew, Video
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
    print(popularTopKeyword)
    topPopularKeywords=[]
    for popularKeyword in popularTopKeyword:
        print(popularKeyword.idx)
        # print(VideoKeywordNew.objects.filter(video_idx=popularKeyword.idx))
        keyword = [keywords.keyword for keywords in popularKeyword.videokeywordnew.all()]
        topPopularKeywords.append(keyword)
    topPopularKeywords=list(itertools.chain(*topPopularKeywords))
    counter=collections.Counter(topPopularKeywords)
    topPopularKeywords=dict(counter.most_common(n=10))
    topPopularKeywords=[{"name":key,"value":topPopularKeywords[key]} for key in topPopularKeywords.keys()]
    topPopularKeywords=[Keyword(keyword=keyword) for keyword in topPopularKeywords]
    topkeywordCountSerializer=KeywordCountSerializer(topPopularKeywords,many=True)
    return Response(topkeywordCountSerializer.data)