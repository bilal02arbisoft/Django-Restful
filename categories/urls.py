from django.urls import path
from categories.views import (CategoryListCreateView, CategoryDetailUpdateView,
                              SubCategoryByCategoryListCreateView, SubCategoryDetailView,
                              SubCategoryListView)

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='categories-list-create'),
    path('categories/<int:pk>/', CategoryDetailUpdateView.as_view(), name='category-detail'),
    path('subcategories/<int:category_id>/', SubCategoryByCategoryListCreateView.as_view(), name='subcategories-list-create'),
    path('subcategories/', SubCategoryListView.as_view(), name='subcategory'),
    path('categories/subcategories/<int:pk>/', SubCategoryDetailView.as_view(), name='subcategory-detail')

]
