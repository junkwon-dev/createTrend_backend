from django.shortcuts import render
from .documents import VideoDocument
from rest_framework.response import Response

from rest_framework.decorators import api_view
from elasticsearch_dsl import Q
# Create your views here.
@api_view(["GET"])
def keyword(request):
    search = request.query_params.get("search")
    s=VideoDocument.search().filter('nested',path='videokeywordnews',query=Q('term', videokeywordnews__keyword=search)).filter('range',upload_time={'gte':'now-7d/d','lt':"now"}).sort({"popularity":"desc"})[:100]
    returnlist=[]
    print(s)
    for hit in s:
        print(
            "Video name : {}".format(hit.video_name)
        )
        returnlist.append({"video":hit.video_name,"upload_time":hit.upload_time,"popularity":hit.popularity})
    return Response(returnlist)