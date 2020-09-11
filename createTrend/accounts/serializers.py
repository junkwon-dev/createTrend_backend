from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserInfo
from django.contrib.auth import authenticate




class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ("id", "phone", "on_subscribe", "own_channel","user_id")
# 접속 유지중인지 확인
class UserSerializer(serializers.ModelSerializer):
    userinfo=UserInfoSerializer(read_only=True)
    class Meta:
        model = User
        fields = ("id", "username","userinfo")

# 회원가입
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"], None, validated_data["password"]
        )
        return user


# 로그인
class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")
    

