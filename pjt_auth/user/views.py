from django.contrib.auth.models import User, Group  
from rest_framework import viewsets  
from user.serializers import UserSerializer, GroupSerializer

# 사용자 목록을 화면에 뿌려주는 ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# 그룹목록을 화면에 뿌려주는 ViewSet
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer