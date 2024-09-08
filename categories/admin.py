from categories.models import Category, SubCategory
from django.contrib import admin


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('name', 'description')
    search_fields = ('name',)


class SubCategoryAdmin(admin.ModelAdmin):
    model = SubCategory
    list_display = ('name', 'description')
    search_fields = ('name',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
