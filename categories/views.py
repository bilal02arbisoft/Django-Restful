
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from categories.models import Category, SubCategory
from categories.serializers import CategorySerializer, SubCategorySerializer
from django.shortcuts import get_object_or_404


class CategoryListCreateView(APIView):

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailUpdateView(APIView):

    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, context={'request': request})
        return Response(serializer.data)

    def patch(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubCategoryByCategoryListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, category_id):

        category = Category.objects.get(id=category_id)
        subcategories = SubCategory.objects.filter(category=category)
        serializer = SubCategorySerializer(subcategories, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, category_id):

        category = Category.objects.get(id=category_id)
        serializer = SubCategorySerializer(data=request.data, context={'request': request, 'category': category})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubCategoryListView(APIView):

    def get(self, request):
        subcategories = SubCategory.objects.all()
        serializer = SubCategorySerializer(subcategories, many=True, context={'request': request})
        return Response(serializer.data)


class SubCategoryDetailView(APIView):

    def get(self, request, pk):

        subcategory = get_object_or_404(SubCategory, id=pk)
        serializer = SubCategorySerializer(subcategory, context={'request': request})
        return Response(serializer.data)

    def patch(self, request, pk):
        subcategory = get_object_or_404(SubCategory, id=pk)

        serializer = SubCategorySerializer(subcategory, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
