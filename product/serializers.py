from rest_framework import serializers
from .models import Category, Product, Review
from django.db.models import Avg


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

    def get_products_count(self, obj):
        return obj.products.count()

# ЭТОТ КЛАСС НУЖНО ДОБАВИТЬ/ВЕРНУТЬ:
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars']

class ProductReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'reviews', 'rating']

    def get_rating(self, obj):
        from django.db.models import Avg
        avg = obj.reviews.aggregate(Avg('stars'))['stars__avg']
        return avg if avg else 0

