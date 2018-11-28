from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import get_hasher
from django.utils.crypto import get_random_string
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()
UNUSABLE_PASSWORD_PREFIX = '!'  # This will never be a valid encoded hash
UNUSABLE_PASSWORD_SUFFIX_LENGTH = 40  # number of random chars to add after UNUSABLE_PASSWORD_PREFIX


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
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

    # def save(self):
    #     username = self.validated_data['username']
    #     password = self.validated_data['password']
    #     first_name = self.validated_data['first_name']
    #     last_name = self.validated_data['last_name']
    #     img_profile = self.validated_data['img_profile']
    #     phone = self.validated_data['phone']
    #     User.objects.create(
    #         username=username,
    #         password=password,
    #         first_name=first_name,
    #         last_name=last_name,
    #         img_profile=img_profile,
    #         phone=phone,
    #     )


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
