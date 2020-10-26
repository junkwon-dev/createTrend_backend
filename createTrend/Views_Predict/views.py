import json
import time
import uuid

import pika
from rest_framework.response import Response
from rest_framework.decorators import api_view



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
            returnDict = {'oneDay':views[0],'twoDay':views[1],'threeDay':views[2],'fourDay':views[3],'fiveDay':views[4],'sixDay':views[5],'sevenDay':views[6],'eightDay':views[7],'nineDay':views[8],'tenDay':views[9],'elevenDay':views[10],'twelveDay':views[11],'thirteenDay':views[12],'fourteenDay':views[13],'fifteenDay':views[14],'sixteenDay':views[15],'seventeenDay':views[16],'eighteenDay':views[17],'ninteenDay':views[18],'twentyDay':views[19],'twentyoneDay':views[20],'twentytwoDay':views[21],'twentythreeDay':views[22],'twentyfourDay':views[23],'twentyfiveDay':views[24],'twentysixDay':views[25],'twentysevenDay':views[26],'twentyeightDay':views[27],'twentynineDay':views[28],'thirtyDay':views[29],'thirtyoneDay':views[30]}
            return Response(returnDict)
        else:
            return Response()

            