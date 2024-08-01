from django.urls import path
from categories.views import (CategoryListCreateView, CategoryDetailView,
                              SubCategoryListCreateView, SubCategoryDetailView)

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='categories-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('subcategories/<int:category_id>/', SubCategoryListCreateView.as_view(), name='subcategories-list-create'),
    path('categories/subcategories/<int:pk>/', SubCategoryDetailView.as_view(), name='subcategory-detail')

]
