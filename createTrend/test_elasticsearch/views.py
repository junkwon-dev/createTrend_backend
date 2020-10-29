from django.shortcuts import render
from .documents import VideoDocument
from rest_framework.response import Response

from rest_framework.decorators import api_view
from elasticsearch_dsl import Q, A
# Create your views here.
@api_view(["GET"])
def keyword(request):
    search = request.query_params.get("search")
    # s=VideoDocument.search().filter('nested',path='videokeywordnews',query=Q('term', videokeywordnews__keyword=search)).filter('range',upload_time={'gte':'now-7d/d','lt':"now"})
    s=VideoDocument.search().filter('term', videokeywordnews__keyword=search).filter('range',upload_time={'gte':'now-14d/d','lt':"now"})
    s.aggs.bucket('uploads_per_day',A('date_histogram',field='upload_time',calendar_interval='1d'))\
        .metric('popularity_per_day', A('avg', field='popularity'))
    response=s.execute()
    
    print(s.to_dict())
    returnlist=[]
    for tag in response.aggregations.uploads_per_day.buckets:
        print(tag.popularity_per_day)
        returnlist.append({'date':tag.key_as_string[:10],'count':tag.doc_count,'popularity':tag.popularity_per_day.value})
    return Response(returnlist)