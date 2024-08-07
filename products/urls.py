from products.views import ProductListView, ProductByCategoryView, ProductBySubCategoryView
from django.urls import path

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('subcategory/<int:subcategory_id>/', ProductBySubCategoryView.as_view(), name='product-by-subcategory'),
    path('category/<int:category_id>/', ProductByCategoryView.as_view(), name='product-by-category'),
]
