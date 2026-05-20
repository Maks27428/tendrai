from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def register(request):
    nickname = request.data.get('nickname', '').strip()
    password = request.data.get('password', '')

    if not nickname:
        return Response({'error': 'Введите никнейм'}, status=status.HTTP_400_BAD_REQUEST)
    if len(password) < 8:
        return Response({'error': 'Пароль должен быть не менее 8 символов'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=nickname).exists():
        return Response({'error': 'Этот никнейм уже занят'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=nickname, password=password)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'nickname': user.username}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login_view(request):
    nickname = request.data.get('nickname', '').strip()
    password = request.data.get('password', '')

    user = authenticate(username=nickname, password=password)
    if not user:
        return Response({'error': 'Неверный никнейм или пароль'}, status=status.HTTP_400_BAD_REQUEST)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'nickname': user.username})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    return Response({'id': request.user.id, 'nickname': request.user.username})
