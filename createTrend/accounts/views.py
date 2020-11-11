from django.shortcuts import render
from .models import User
# Create your views here.
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from knox.models import AuthToken
from .serializers import CreateUserSerializer, UserSerializer, LoginUserSerializer, UserInfoSerializer


# Create your views here.

class RegistrationAPI(generics.GenericAPIView):
    '''
        회원 가입 API
        ---
        회원 가입을 할 때 사용하는 API입니다.
    '''
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        if len(request.data["username"]) < 5 or len(request.data["password"]) < 4:
            body = {"message": "short field"}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


class LoginAPI(generics.GenericAPIView):
    '''
            로그인 API
            ---
            로그인을 할 때 사용하는 API입니다.
        '''
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserInfoUpdateAPI(generics.UpdateAPIView):
    '''
        사용자 정보 업데이트 API
        ---
        사용자의 상세 정보를 기입하거나, 정보를 업데이트 할 때 사용하는 API입니다.
    '''
    model = User
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserInfoSerializer

    def get_object(self, queryset=None):
        return self.request.user.userinfo

    def update(self, request, *args, **kwargs):
        user_info_object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_info_object.set_phone(serializer.data.get("phone"))
            user_info_object.set_on_subscribe(serializer.data.get("on_subscribe"))
            user_info_object.set_own_channel(serializer.data.get("own_channel"))
            user_info_object.save()
        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'User info updated successfully',
            'data': []
        }
        return Response(response)
