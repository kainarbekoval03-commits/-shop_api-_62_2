from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, Review
from .serializers import CategorySerializer, ReviewSerializer, ProductReviewSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Count
import random
from .serializers import RegisterSerializer
from django.contrib.auth.models import User
from .models import UserConfirm
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

@api_view(['PUT', 'DELETE'])
def category_detail(request, id):
    category = get_object_or_404(Category, id=id)

    if request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=204)

@api_view(['GET'])
def category_list(request):
    categories = Category.objects.annotate(products_count=Count('products'))
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def category_create(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductReviewSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors)

@api_view(['PUT', 'DELETE'])
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'PUT':
        serializer = ProductReviewSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=204)

@api_view(['GET'])
def products_with_reviews(request):
    products = Product.objects.all()
    serializer = ProductReviewSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def product_create(request):
    serializer = ProductReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors)

@api_view(['POST'])
def review_create(request):
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors)

@api_view(['GET'])
def review_list(request):
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)


@api_view(['POST', 'DELETE'])
def review_detail(request, id):
    review = get_object_or_404(Review, id=id)

    if request.method == 'POST':
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == 'DELETE':
        review.delete()
        return Response(status=204)
    
@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        code = str(random.randint(100000, 999999))

        UserConfirm.objects.create(
            user=user,
            code=code
        )

    
        return Response({
            "message": "User created. Confirm your account",
            "code": code   
        })

    return Response(serializer.errors, status=400)

@api_view(['POST'])
def confirm_user(request):
    username = request.data.get('username')
    code = request.data.get('code')

    try:
        user = User.objects.get(username=username)
        confirm = UserConfirm.objects.get(user=user)

        if confirm.code != code:
            return Response({"error": "Wrong code"}, status=400)

        user.is_active = True
        user.save()

        confirm.is_confirmed = True
        confirm.save()

        return Response({"message": "User confirmed"})

    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({"error": "Invalid credentials"}, status=400)

    if not user.is_active:
        return Response({"error": "User not confirmed"}, status=403)

    token, created = Token.objects.get_or_create(user=user)

    return Response({
        "token": token.key
    })