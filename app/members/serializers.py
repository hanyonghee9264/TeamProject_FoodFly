from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed


User = get_user_model()


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
