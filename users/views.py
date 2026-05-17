import random
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer, ConfirmSerializer
from .redis_client import save_confirmation_code, get_confirmation_code, delete_confirmation_code


@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        code = str(random.randint(100000, 999999))
        save_confirmation_code(user.email, code)

        return Response({
            "message": "User created. Confirm your account.",
            "code": code
        })

    return Response(serializer.errors, status=400)


@api_view(['POST'])
def confirm_user(request):
    serializer = ConfirmSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    email = serializer.validated_data['email']
    code = serializer.validated_data['code']

    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    stored_code = get_confirmation_code(email)

    if stored_code is None:
        return Response({"error": "Code expired or not found"}, status=400)

    if stored_code != code:
        return Response({"error": "Wrong code"}, status=400)

    delete_confirmation_code(email)

    user.is_active = True
    user.save()

    return Response({"message": "User confirmed"})


@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    email = serializer.validated_data['email']
    password = serializer.validated_data['password']

    user = authenticate(request, email=email, password=password)

    if user is None:
        return Response({"error": "Invalid credentials"}, status=400)

    if not user.is_active:
        return Response({"error": "User not confirmed"}, status=403)

    token, _ = Token.objects.get_or_create(user=user)

    return Response({"token": token.key})
