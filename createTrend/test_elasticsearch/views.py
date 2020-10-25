from django.shortcuts import render
from .documents import VideoDocument
from rest_framework.response import Response

from rest_framework.decorators import api_view

# Create your views here.
@api_view(["GET"])
def keyword(request):
    s=VideoDocument.search().query("term",videokeywordnews__keyword="챌린저")
    for hit in s:
        print(
            "Video name : {}".format(hit.video_name)
        )
        for video_keyword in hit.videokeywordnews:
            print(video_keyword)
    return Response({'a':'b'})