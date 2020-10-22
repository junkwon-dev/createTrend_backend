from django.shortcuts import render
from .models import Video
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.utils import timezone
from datetime import datetime, timedelta
import datetime, itertools, collections, time

from django.db.models import Avg
from rest_framework.decorators import api_view
from .serializers import VideoViewsSerializer, VideoSerializer, ChannelSerializer
##전체평균인기도(일주일) 전체평균조회수(일주일) 해당동영상 조회수(일주일) 

# Create your views here.
@api_view(['GET'])
def videoDetail(request,pk):
    try:
        video = Video.objects\
            .get(pk=pk)
    except Video.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        start = timezone.now() - datetime.timedelta(days=14)
        start = start.strftime("%Y-%m-%d")
        end = timezone.now().strftime("%Y-%m-%d")
        avg_popularity=Video.objects.filter(upload_time__range=(start, end)).aggregate(Avg('popularity'))
        avg_videoviews=Video.objects.filter(upload_time__range=(start, end)).aggregate(Avg('views'))
        video_views=video.views 
        video_views_transition=[]
        video_views_querysets=list(video.videoviews.all())
        for video_views_queryset in video_views_querysets:
            video_views_transition.append({"date":str(video_views_queryset.check_time)[:10],"value":video_views_queryset.views})
        video_popularity=video.popularity
        channel = video.channel_idx
        serialized_video = VideoSerializer(video)
        serialzied_channel = ChannelSerializer(channel)
        return Response({"type":"영상","video":{'video_views':video_views,'video_popularity':video_popularity,'avg_popularity':avg_popularity['popularity__avg'],'avg_videoviews':avg_videoviews['views__avg'], 'video':serialized_video.data}
                         ,'lines':{'type':"조회수 추이","data":video_views_transition},'channel':serialzied_channel.data})
        