from django.shortcuts import render
from rest_framework import viewsets  
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from Search_Keyword.serializers import ChannelListSerializer, VideoKeywordSerializer
from .models import Channel, VideoKeywordNew
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
            queryset = VideoKeywordNew.objects.filter(keyword__icontains=search)
            paginator = PageNumberPagination()
            paginator.page_size = 10
            result_page = paginator.paginate_queryset(queryset, request)
            serializer = VideoKeywordSerializer(result_page,many=True)
            return paginator.get_paginated_response(serializer.data) 
        else:
            paginator = PageNumberPagination()
            paginator.page_size = 10
            queryset = VideoKeywordNew.objects.all()
            result_page = paginator.paginate_queryset(queryset, request)
            serializer = VideoKeywordSerializer(result_page,many=True)
            return paginator.get_paginated_response(serializer.data) 

      
