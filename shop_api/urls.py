"""
URL configuration for shop_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from product.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/categories/', CategoryListView.as_view()),
    path('api/v1/categories/<int:id>/', CategoryDetailView.as_view()),
    path('api/v1/categories/create/', category_create),

    path('api/v1/products/', ProductListView.as_view()),
    path('api/v1/products/<int:id>/', ProductDetailView.as_view()),
    path('api/v1/products/reviews/', products_with_reviews),
    path('api/v1/poducts/create/', product_create),


    path('api/v1/reviews/', ReviewListView.as_view()),
    path('api/v1/reviews/<int:id>/', ReviewDetailView.as_view()),
    path('api/v1/reviews/create/', review_create),
    


    path('api/v1/users/register/', register),
    path('api/v1/users/confirm/', confirm_user),
    path('api/v1/users/login/', login),
]


