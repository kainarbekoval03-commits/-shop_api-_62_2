from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, Product, Review
from .serializers import CategorySerializer, ReviewSerializer, ProductReviewSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Count
import random
from django.contrib.auth.models import User
from .models import UserConfirm
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

class CategoryDetailView(APIView):

    def get(self, request, id):
        category = get_object_or_404(Category, id=id)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, id):
        category = get_object_or_404(Category, id=id)
        serializer = CategorySerializer(category, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, id):
        category = get_object_or_404(Category, id=id)
        category.delete()
        return Response(status=204)

class CategoryListView(APIView):

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['POST'])
def category_create(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

class ProductListView(APIView):

    def get(self, request):
        category_id = request.GET.get('category')

        if category_id:
            products = Product.objects.filter(category_id=category_id)
        else:
            products = Product.objects.all()

        serializer = ProductReviewSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductReviewSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors)

class ProductDetailView(APIView):

    def get(self, request, id):
        product = get_object_or_404(Product, id=id)
        serializer = ProductReviewSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        product = get_object_or_404(Product, id=id)
        serializer = ProductReviewSerializer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    def delete(self, request, id):
        product = get_object_or_404(Product, id=id)
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

class ReviewListView(APIView):

    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors)


class ReviewDetailView(APIView):

    def get(self, request, id):
        review = get_object_or_404(Review, id=id)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    def put(self, request, id):
        review = get_object_or_404(Review, id=id)
        serializer = ReviewSerializer(review, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    def delete(self, request, id):
        review = get_object_or_404(Review, id=id)
        review.delete()
        return Response(status=204)
    
@api_view(['POST'])
def register(request):
    serializer = ReviewSerializer(data=request.data)

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