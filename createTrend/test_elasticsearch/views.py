from django.shortcuts import render
from .documents import VideoDocument
from rest_framework.response import Response

from rest_framework.decorators import api_view

# Create your views here.
@api_view(["GET"])
def keyword(request):
    search = request.query_params.get("search")
    s=VideoDocument.search().query("term",videokeywordnews__keyword=search)
    returnlist=[]
    for hit in s:
        print(
            "Video name : {}".format(hit.video_name)
        )
        keywordlist=[]
        for video_keyword in hit.videokeywordnews:
            print(video_keyword)
            keywordlist.append({'keyword':video_keyword})
        returnlist.append({"video_name" : hit.video_name,"keywordlist":keywordlist})
    return Response(returnlist)