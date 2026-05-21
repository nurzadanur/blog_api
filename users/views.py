from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserAuthSerializer


@swagger_auto_schema(method='post', request_body=UserRegisterSerializer)
@api_view(['POST'])
def registration_api_view(request):
    serializer = UserRegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    user = User.objects.create_user(
        username=username,
        password=password
    )
    token = Token.objects.create(user=user)
    return Response(
        status=status.HTTP_201_CREATED,
        data={
            'user_id': user.id,
            'token': token.key,
        }
    )


@swagger_auto_schema(method='post', request_body=UserAuthSerializer)
@api_view(['POST'])
def authorization_api_view(request):
    serializer = UserAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response(data={'token': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED)
