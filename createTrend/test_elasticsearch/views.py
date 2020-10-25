from django.shortcuts import render
from .documents import VideoDocument
from rest_framework.response import Response

from rest_framework.decorators import api_view
from elasticsearch_dsl import Q
# Create your views here.
@api_view(["GET"])
def keyword(request):
    search = request.query_params.get("search")
    s=VideoDocument.search().filter('nested',path='videokeywordnews',query=Q('term', videokeywordnews__keyword=search))
    returnlist=[]
    print(s)
    for hit in s:
        print(
            "Video name : {}".format(hit.video_name)
        )
        returnlist.append({"video":hit.video_name})
    return Response(returnlist)