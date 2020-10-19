from django.shortcuts import render
from rest_framework.response import Response

@api_view(['GET'])
def videoPredict(request,pk):
    if request.method == 'GET':
        thumbnail_url = request.query_params.get("thumbnail_url")
        video_name = request.query_params.get("video_name")
        channel_subscriber = request.query_params.get("channel_subscriber")
        upload_date = request.query_params.get("upload_date")
        if thumbnail_url and video_name and channel_subscriber and upload_date:
            return Response()
        else:
            return Response()
            