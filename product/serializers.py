from rest_framework import serializers
from .models import Category, Product, Review
from django.db.models import Avg


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars']


class ProductReviewSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'reviews', 'rating']

    def get_rating(self, obj):
        avg = obj.reviews.aggregate(avg=Avg('stars'))['avg']
        return round(avg, 1) if avg else 0
