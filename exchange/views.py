from django.shortcuts import render

from rest_framework import viewsets

from exchange.models import Category
from exchange.serializer import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


