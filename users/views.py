from django.http import JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import User
import json

@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        name = data.get('name')
        username = data.get('username')
        password = data.get('password')

        if not email or not name or not username or not password:
            return JsonResponse({'error': 'All fields are required.'}, status=400)

        user = User(email=email, name=name, username=username, password=password)
        user.save()
        return JsonResponse({'message': 'User registered successfully.'}, status=201)
    except IntegrityError:
        return JsonResponse({'error': 'Email or username already exists.'}, status=400)
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Something went wrong.'}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_users(request):
    users = User.objects.all().values('user_id', 'email', 'name', 'username', 'is_event_manager')
    return JsonResponse(list(users), safe=False)

@csrf_exempt
@require_http_methods(["GET"])
def get_user_by_id(request, user_id):
    try:
        user = User.objects.values('user_id', 'email', 'name', 'username', 'is_event_manager').get(user_id=user_id)
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