from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import analyzer
from .models import VideoKeywordNew, Video


nori_analyzer = analyzer(
    'nori_analyzer',
    tokenizer= "nori_tokenizer",
    filter=["lowercase", "stop"],
)

# @registry.register_document
# class VideoKeywordNewDocument(Document):
#     video_idx = fields.ObjectField(properties={
#         'idx' :fields.IntegerField(),
#         'video_name' : fields.TextField(),
#         'video_description' : fields.TextField(),
#         'video_id' : fields.TextField(),
#         'upload_time' : fields.DateField(),
#         'thumbnail_url' : fields.TextField(),
#         'popularity' : fields.DoubleField(),
#         'views' : fields.IntegerField(),
#         'views_growth' : fields.IntegerField(),
#         'crawled' : fields.BooleanField(),
#     })
#     keyword = fields.TextField(
#         analyzer=nori_analyzer
#     )
#     class Index:
#         name='videokeywordnews'
        
#     class Django:
#         model = VideoKeywordNew
#         fields =[
#             'idx',
#             'keyword',
#         ]
#         related_models = [Video]
        
#     def get_queryset(self):
#         return super(VideoKeywordNewDocument, self).get_queryset().select_related(
#             'video_idx'
#         )
    
#     def get_instances_from_related(self, related_instance):
#         if isinstance(related_instance, Video):
#             return related_instance.VideoKeywordNew_set.all()

@registry.register_document
class VideoDocument(Document):
    videokeywordnews=fields.NestedField(properties={
        'idx': fields.IntegerField(),
        'keyword' : fields.TextField(analyzer=nori_analyzer),
    })
    
    class Index:
        name='videos'
        
    class Django:
        model = Video
        fields =[
            'idx',
            'video_name',
            'video_description',
            'video_id',
            'upload_time',
            'thumbnail_url',
            'popularity',
            'views',
            'views_growth',
            'crawled',
        ]
        related_models = [VideoKeywordNew]

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, VideoKeywordNew):
            return related_instance.video
        
        
