import pytz
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from address.models import Address
from address.serializers import AddressInfoSerializer
from .backends import FacebookBackend


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()

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
            'address'
        )

    def get_address(self, obj):
        if not Address.objects.filter(user=obj).exists():
            return
        else:
            address = Address.objects.filter(user=obj)
            return AddressInfoSerializer(address, many=True).data


class UserRegisterSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + (
            'password',
        )

    def create(self, validate_data):
        user = User.objects.create_user(
            **validate_data,
        )
        return user


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
    name = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=50)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def create(self, validate_data):
        username = validate_data['facebook_id']
        password = 'foodfly'
        name = validate_data['name']
        email = validate_data['email']

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
        else:
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=name,
                email=email,
            )
        self.user = user
        return self.user

    def to_representation(self, instance):
        token = Token.objects.get_or_create(user=self.user)[0]
        data = {
            'user': UserSerializer(self.user).data,
            'token': token.key,
        }
        return data
