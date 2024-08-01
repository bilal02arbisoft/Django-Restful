from django.contrib import admin
from .models import Product, ProductVariant, Attribute, AttributeValue, ProductVariantAttribute


class ProductVariantAttributeInline(admin.TabularInline):
    model = ProductVariantAttribute
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'subcategory', 'has_variants', 'price', 'stock', 'created_at', 'updated_at')
    search_fields = ('name', 'subcategory__name', 'description')
    list_filter = ('subcategory', 'has_variants')
    inlines = [ProductVariantInline]

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.has_variants:
            return self.readonly_fields + ('price', 'stock')
        return self.readonly_fields

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj and obj.has_variants:
            fields.remove('price')
            fields.remove('stock')
        return fields


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'sku', 'price', 'stock')
    search_fields = ('product__name', 'sku')
    list_filter = ('product',)
    inlines = [ProductVariantAttributeInline]


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ('attribute', 'value')
    search_fields = ('attribute__name', 'value')
    list_filter = ('attribute',)


@admin.register(ProductVariantAttribute)
class ProductVariantAttributeAdmin(admin.ModelAdmin):
    list_display = ('variant', 'attribute_value')
    search_fields = ('variant__sku', 'attribute_value__value')
    list_filter = ('variant', 'attribute_value')
