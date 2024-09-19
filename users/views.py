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
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import User

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
    users = User.objects.all().values('id', 'email', 'name', 'is_event_manager')
    return JsonResponse(list(users), safe=False)

@csrf_exempt
@require_http_methods(["GET"])
def get_user_by_id(request, user_id):
    try:
        user = User.objects.values('id', 'email', 'name', 'is_event_manager').get(id=user_id)
        return JsonResponse(user, safe=False)
    except User.DoesNotExist:
        return HttpResponseNotFound({'error': 'User not found.'})
    except Exception as e:
        return JsonResponse({'error': 'Something went wrong.'}, status=500)
    

class DeleteUserView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def delete(self, request):
        try:
            # Extract the user ID from the token
            user_id = request.user.id

            # Get the user object
            user = User.objects.get(id=user_id)

            # Delete the user
            user.delete()

            return Response({'message': 'User deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)