from django.shortcuts import render
from rest_framework import viewsets  
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from django.db.models import Max 
from Search_Keyword.serializers import ChannelListSerializer, VideoKeywordSerializer, TopVideoSerializer\
    ,RecentVideoSerializer, KeywordCountSerializer
from .models import Channel, VideoKeywordNew, Video
from rest_framework.response import Response
import datetime, itertools, collections
# from Search_Keyword.serializers import topComment
# Create your views here.
# class topCommentViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

@api_view(['GET'])
def keyword(request):
    if request.method == 'GET':
        search=request.query_params.get('search')
        if search:
            start=datetime.datetime.now()-datetime.timedelta(days=14)
            start=start.strftime("%Y-%m-%d")
            end=datetime.datetime.now().strftime("%Y-%m-%d")
            topVideo =Video.objects.all()\
                .filter(videokeywordnew__keyword=search, upload_time__range=(start,end))\
                .annotate(Max('videoviews__check_time'))\
                .order_by('-videoviews__views')[:10] 
            recentVideo = Video.objects.all()\
                .filter(videokeywordnew__keyword=search, upload_time__range=(start,end))\
                .annotate(Max('videoviews__check_time'))\
                .order_by('-videoviews__check_time')[:10]  
            
            # videos = channel.video.all().prefetch_related('videokeyword')
            keywordVideo=Video.objects.all()\
                .filter(videokeywordnew__keyword=search, upload_time__range=(start,end))\
                .annotate(Max('videoviews__check_time'))\
                .order_by('-videoviews__check_time')[:10].prefetch_related('videokeywordnew')  
            keywords=[]

            for video in keywordVideo:
                keyword=[videokeyword.keyword for videokeyword in video.videokeywordnew.all()]
                keywords.append(keyword)
            keywords=list(itertools.chain(*keywords))
            while search in keywords:
                keywords.remove(search)
            counter=collections.Counter(keywords)
            keywords=dict(counter.most_common(n=20))
            keywords=[{"name":key,"value":keywords[key]} for key in keywords.keys()]
            class Keyword(object):
                def __init__(self,keyword):
                    self.name = keyword['name']
                    self.value=keyword['value']
            keywords=[Keyword(keyword=keyword) for keyword in keywords]

            keywordCountSerializer=KeywordCountSerializer(keywords,many=True)
                        
            topVideoSerializer = TopVideoSerializer(topVideo,many=True)
            recentVideoSerializer = RecentVideoSerializer(topVideo,many=True)
            return Response({'video':[{"type":"analysis","data":topVideoSerializer.data},\
                {"type":"analysis","data":recentVideoSerializer.data}], 'wordmap':{'name':search,'children':keywordCountSerializer.data}}) 
        else:
            paginator = PageNumberPagination()
            paginator.page_size = 10
            queryset = VideoKeywordNew.objects.all()
            result_page = paginator.paginate_queryset(queryset, request)
            serializer = VideoKeywordSerializer(result_page,many=True)
            return paginator.get_paginated_response(serializer.data) 

      
