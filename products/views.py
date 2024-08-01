
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from categories.models import Category, SubCategory
from products.serializers import ProductSerializer
from products.models import Product


class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductBySubCategoryView(APIView):
    def get(self, request, subcategory_id):
        try:
            subcategory = SubCategory.objects.get(pk=subcategory_id)
            products = Product.objects.filter(subcategory=subcategory)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except SubCategory.DoesNotExist:
            return Response({"error": "SubCategory not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, subcategory_id):
        try:
            SubCategory.objects.get(pk=subcategory_id)
        except SubCategory.DoesNotExist:
            return Response({"error": "SubCategory not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductByCategoryView(APIView):
    def get(self, request, category_id):
        try:
            category = Category.objects.get(pk=category_id)
            subcategories = SubCategory.objects.filter(category=category)
            products = Product.objects.filter(subcategory__in=subcategories)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)






