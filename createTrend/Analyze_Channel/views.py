from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from . import functions as f

param_keyword_data_search_hint = openapi.Parameter(
    'search',
    openapi.IN_QUERY,
    description='영상화 혹은 인기 키워드를 검색합니다. 영상화 혹은 인기 를 입력하세요.',
    type=openapi.TYPE_STRING
)
param_keyword_data_keyword_hint = openapi.Parameter(
    'keyword',
    openapi.IN_QUERY,
    description='검색하고 싶은 키워드를 입력하세요.',
    type=openapi.TYPE_STRING
)


@swagger_auto_schema(method='get', manual_parameters=[param_keyword_data_search_hint, param_keyword_data_keyword_hint])
@api_view(['GET'])
def keyword_data(request):
    '''
    전체 채널 인기,영상화 TOP10 키워드 API
    ---
    전체 채널 TOP10 키워드를 클릭할 때 키워드의 인기도, 영상화 수치, 추이 등을 제공하는 API입니다.
    '''
    search = request.query_params.get('search')
    keyword = request.query_params.get('keyword')

    # 영상화 및 인기에 따른 데이터들 추출, 가공 및 직렬화
    if (search == '영상화' and keyword):
        return f.channel_imaging_keyword(keyword)
    elif (search == '인기' and keyword):
        return f.channel_popular_keyword(keyword)


@api_view(['GET'])
def analyze_channel(request):
    '''
    전체 채널 인기,영상화 TOP10 키워드 API
    ---
    전체 채널 중 인기, 영상화 TOP 10 키워드를 제공하는 API입니다.
    '''
    # 인기 키워드 탑10 데이터 추출, 가공 및 직렬화
    popular_top10_keyword = f.get_popular_top10_keyword()
    # 영상화 키워드 탑10 데이터 추출, 가공 및 직렬화
    imaging_top10_keyword = f.get_imaging_top10_keyword()
    return Response([popular_top10_keyword,
                     imaging_top10_keyword])
