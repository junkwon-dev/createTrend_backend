from django.shortcuts import render
from rest_framework import viewsets  
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from Search_Keyword.serializers import ChannelListSerializer
# from Search_Keyword.serializers import topComment
# Create your views here.
# class topCommentViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

@api_view(['GET'])
def channellist(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10
    queryset = Channel.objects.all()
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = ChannelListSerializer(result_page,many=True)
    return paginator.get_paginated_response(serializer.data) 
      
