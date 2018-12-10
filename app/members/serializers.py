from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from .backends import FacebookBackend

User = get_user_model()
UNUSABLE_PASSWORD_PREFIX = '!'  # This will never be a valid encoded hash
UNUSABLE_PASSWORD_SUFFIX_LENGTH = 40  # number of random chars to add after UNUSABLE_PASSWORD_PREFIX


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'nickname',
            'first_name',
            'last_name',
            'img_profile',
            'phone',
        )


class UserRegisterSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + (
            'password',
        )

    def save(self):
        username = self.validated_data['username']
        password = self.validated_data['password']
        nickname = self.validated_data['nickname']
        User.objects.create_user(
            username=username,
            password=password,
            nickname=nickname,
        )


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self, data):
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user is None:
            raise AuthenticationFailed('아이디 또는 비밀번호가 일치하지 않습니다.')
        self.user = user
        return data

    def to_representation(self, instance):
        token = Token.objects.get_or_create(user=self.user)[0]
        data = {
            'user': UserSerializer(self.user).data,
            'token': token.key,
        }
        return data


class FacebookSerializer(serializers.Serializer):
    facebook_id = serializers.CharField(max_length=50)
    access_token = serializers.CharField(max_length=50)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self, data):
        facebook_id = data['facebook_id']
        access_token = data['access_token']
        if User.objects.filter(username=facebook_id).exists():
            user = User.objects.get(username=facebook_id)
        else:
            user = FacebookBackend.get_user_by_access_token(access_token)
        self.user = user
        return data

    def to_representation(self, instance):
        token = Token.objects.get_or_create(user=self.user)[0]
        data = {
            'user': UserSerializer(self.user).data,
            'token': token.key,
        }
        return data
