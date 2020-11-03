import json
import time
import uuid

import pika
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils import timezone
from datetime import datetime, timedelta
import datetime, itertools, collections, time
from .documents import VideoDocument
from .models import Video,Channel
from elasticsearch_dsl import Q


@api_view(['POST'])
def videoViewsPredict(request):
    if request.method == 'POST':    
        thumbnail_url = request.data["thumbnail_url"]
        video_name = request.data["video_name"]
        channel_subscriber = request.data["channel_subscriber"]
        upload_date = request.data["upload_date"]
        print(thumbnail_url, video_name,channel_subscriber,upload_date)
        if thumbnail_url and video_name and channel_subscriber and upload_date:
            

            credentials = pika.PlainCredentials("muna", "muna112358!")
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    "13.124.107.195",
                    5672,
                    "/",
                    credentials,
                    heartbeat=10,
                    blocked_connection_timeout=10,
                )
            )
            channel = connection.channel()

            # 각 시도에 따른 고유 ID 생성
            queue_name = str(uuid.uuid4())
            # 해당 ID로 큐 생성하고 데이터 저장
            # AI 서버로 데이터 전송하는 큐
            channel.queue_declare(queue=queue_name, durable=True)
            # AI 서버에서 데이터 받아오는 큐
            channel.queue_declare(queue=queue_name + "_r", durable=True)
            data = [thumbnail_url, video_name, channel_subscriber, upload_date]
            channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(data))

            # 'request_ai_process' 큐에 생성한 ID 저장
            channel.basic_publish(exchange='', routing_key='request_ai_process', body=queue_name)

            # 결과 올때까지 대기
            start_time = time.time()
            done = False
            while time.time() - start_time < 100 and not done:
                method_frame, header_frame, body = channel.basic_get(queue=queue_name + "_r", auto_ack=False)
                print(method_frame,header_frame,body)
                if method_frame == None:
                    time.sleep(0.5)
                    continue
                else:
                    views = json.loads(body)
                    done = True

                    channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                    channel.queue_delete(queue=queue_name + "_r")
                    connection.close()
                    break

            views_predict_transition=[]
            for i in range(31):
                date=timezone.now() + datetime.timedelta(days=i+1)
                date=date.strftime("%Y-%m-%d")
                views_predict_transition.append({'date':date,'value':int(views[i])})
            return Response({'lines':{'type':"조회수 추이","data":views_predict_transition}})
        else:
            return Response()
        
@api_view(['GET'])        
def simple_recommendation(request):
    keyword_string = request.query_params.get("keyword_string")
    res=(VideoDocument.search()
         .filter('match', videokeywordnews__keyword=keyword_string)
         .filter('range',upload_time={'gte':'now-30d/d','lt':"now"})
         .sort({'popularity':"desc"}))[:8]
    idxs=[row.idx for row in res]
    res=[]
    for idx in idxs:
        video=Video.objects.get(pk=idx)
        channel_name=video.channel_idx.channel_name
        channel_thumbnail_url=video.channel_idx.thumbnail_url
        video_thumbnail_url=video.thumbnail_url
        video_name=video.video_name
        res.append({"idx":idx,"channel_name":channel_name,"channel_thumbnail_url":channel_thumbnail_url,"video_thumbnail_url":video_thumbnail_url,"video_name":video_name})
    return Response(res)

@api_view(['GET'])        
def advanced_recommendation(request):
    keyword_string = request.query_params.get("keyword_string")
    must_keyword = request.query_params.get("must_keyword")
    must_not_keyword = request.query_params.get("must_not_keyword")
    must_keyword_list=[]
    must_not_keyword_list=[]
    must_keyword_list.append(keyword_string)
    try:
        must_keyword_list=must_keyword.split(" ")
    except:
        pass
    try:
        must_not_keyword_list=must_not_keyword.split(" ")
        print(must_not_keyword_list)
    except:
        pass

    res = (
        VideoDocument.search()
        .filter("match",videokeywordnews__keyword=keyword_string)
        .exclude("terms",videokeywordnews__keyword=must_not_keyword_list)
        .filter("terms",videokeywordnews__keyword=must_keyword_list)
        .sort({'popularity':"desc"})[:8]
    )
    # .filter("bool",Q("must_not",Q("terms",videokeywordnews__keyword=must_not_keyword_list)))
    idxs=[row.idx for row in res]
    res=[]
    for idx in idxs:
        video=Video.objects.get(pk=idx)
        channel_name=video.channel_idx.channel_name
        channel_thumbnail_url=video.channel_idx.thumbnail_url
        video_thumbnail_url=video.thumbnail_url
        video_name=video.video_name
        res.append({"idx":idx,"channel_name":channel_name,"channel_thumbnail_url":channel_thumbnail_url,"video_thumbnail_url":video_thumbnail_url,"video_name":video_name})
    return Response(res)

    
            