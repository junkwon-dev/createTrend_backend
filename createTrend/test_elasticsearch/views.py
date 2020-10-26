from django.shortcuts import render
from .documents import VideoDocument
from rest_framework.response import Response

from rest_framework.decorators import api_view
from elasticsearch_dsl import Q, A
# Create your views here.
@api_view(["GET"])
def keyword(request):
    search = request.query_params.get("search")
    s=VideoDocument.search().filter('nested',path='videokeywordnews',query=Q('term', videokeywordnews__keyword=search)).filter('range',upload_time={'gte':'now-7d/d','lt':"now"})
    s.aggs.bucket('mola',A('date_histogram',field='upload_time',calendar_interval='1d'))
    response=s.execute()
    print(response.hits.total)
    returnlist=[]
    for tag in response.aggregations.mola.buckets:
        returnlist.append({'date':tag.key_as_string[:10],'count':tag.doc_count})
    return Response(returnlist)