from django.http import JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import User
import json

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer

@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User registered successfully.'}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })
    return Response(serializer.errors, status=401)

@csrf_exempt
@require_http_methods(["GET"])
def get_users(request):
    users = User.objects.all().values('id', 'email', 'name', 'username', 'is_event_manager')
    return JsonResponse(list(users), safe=False)

@csrf_exempt
@require_http_methods(["GET"])
def get_user_by_id(request, user_id):
    try:
        user = User.objects.values('id', 'email', 'name', 'username', 'is_event_manager').get(id=user_id)
        return JsonResponse(user, safe=False)
    except User.DoesNotExist:
        return HttpResponseNotFound({'error': 'User not found.'})
    except Exception as e:
        return JsonResponse({'error': 'Something went wrong.'}, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_user(request, user_id):
    try:
        user = User.objects.get(user_id=user_id)
        user.delete()
        return JsonResponse({'message': 'User deleted successfully.'}, status=200)
    except User.DoesNotExist:
        return HttpResponseNotFound({'error': 'User not found.'})
    except Exception as e:
        return JsonResponse({'error': 'Something went wrong.'}, status=500)