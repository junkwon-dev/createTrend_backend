from rest_framework.decorators import api_view
import time
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from . import functions as f

param_search_hint = openapi.Parameter(
    "search", openapi.IN_QUERY, description="검색하고 싶은 키워드를 입력하세요.", type=openapi.TYPE_STRING,
)
from django.http import HttpResponseNotFound


@swagger_auto_schema(method="get", manual_parameters=[param_search_hint])
@api_view(["GET"])
def keyword(request):
    """
    키워드 검색 API
    ---
    검색한 키워드와 관련된 최근 영상과, 인기있는 영상, 관련 키워드 워드맵 정보 등을 제공하는 api입니다.
    """
    start_time = time.time()
    search = request.query_params.get("search")
    if search:
        return f.search_keyword(search)
    else:
        # 키워드 없을 시 404 not found
        return HttpResponseNotFound("없는 페이지 입니다.")
