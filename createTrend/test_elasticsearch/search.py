from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Document, Text, Date, Integer, Search
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from . import models

connections.create_connection(hosts=['localhost'])

class keywordIndex(Document):
    idx = Integer()
    keyword = Text()
    video_idx = Integer()
    class Index:
        name = 'videokeywordnew-index'
    
def bulk_indexing():
    keywordIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in models.VideoKeywordNew.objects.all().iterator()))
    
def search(display):
    s = Search().filter('match', display = display)
    response = s.execute()
    return response