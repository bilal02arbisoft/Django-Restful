from rest_framework import serializers
from products.models import (Product, ProductVariant, Attribute,
                             AttributeValue, ProductVariantAttribute)


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute = serializers.CharField()

    class Meta:
        model = AttributeValue
        fields = ('attribute', 'value')


class ProductVariantAttributeSerializer(serializers.ModelSerializer):
    attribute_value = AttributeValueSerializer()

    class Meta:
        model = ProductVariantAttribute
        fields = ('variant', 'attribute_value')
        read_only_fields = ['variant']


class ProductVariantSerializer(serializers.ModelSerializer):
    variant_attributes = ProductVariantAttributeSerializer(many=True)

    class Meta:
        model = ProductVariant
        fields = ('id', 'sku', 'price', 'product', 'stock', 'variant_attributes')
        read_only_fields = ['product']


class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'stock', 'subcategory',
                  'has_variants', 'created_at', 'updated_at', 'variants')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate(self, data):
        has_variants = data.get('has_variants', False)
        price = data.get('price')
        stock = data.get('stock')
        if has_variants:

            if price is not None or stock is not None:

                raise serializers.ValidationError("Products with variants should not have a price or stock directly.")
        else:
            if price is None or stock is None:

                raise serializers.ValidationError("Products without variants must have a price and stock.")

        return data

    def create(self, validated_data):
        variants_data = validated_data.pop('variants', None)
        product = Product.objects.create(**validated_data)

        if variants_data:

            for variant_data in variants_data:
                variant_attributes_data = variant_data.pop('variant_attributes')
                variant = ProductVariant.objects.create(product=product, **variant_data)

                for attribute_data in variant_attributes_data:
                    attribute_value_data = attribute_data['attribute_value']
                    attribute_name = attribute_value_data['attribute']
                    value = attribute_value_data['value']
                    attribute_instance, created = Attribute.objects.get_or_create(name=attribute_name)
                    attribute_value_instance, created = AttributeValue.objects.get_or_create(attribute=
                                                                                             attribute_instance,
                                                                                             value=value)
                    ProductVariantAttribute.objects.create(variant=variant, attribute_value=attribute_value_instance)

        return product

    def update(self, instance, validated_data):
        variants_data = validated_data.pop('variants')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if variants_data:

            for variant_data in variants_data:
                variant_id = variant_data.get('id')
                if variant_id:

                    variant = ProductVariant.objects.get(id=variant_id, product=instance)
                    attributes_data = variant_data.pop('variant_attributes', [])
                    for attr, value in variant_data.items():
                        setattr(variant, attr, value)
                    variant.save()
                    for attribute_data in attributes_data:
                        attribute_value_data = attribute_data['attribute_value']
                        attribute, created = Attribute.objects.get_or_create(name=attribute_value_data['attribute'])
                        attribute_value, created = AttributeValue.objects.get_or_create(attribute=attribute,
                                                                                        value=attribute_value_data[
                                                                                            'value'])
                        ProductVariantAttribute.objects.update_or_create(variant=variant,
                                                                         attribute_value=attribute_value)
                else:
                    attributes_data = variant_data.pop('variant_attributes')
                    variant = ProductVariant.objects.create(product=instance, **variant_data)
                    for attribute_data in attributes_data:
                        attribute_value_data = attribute_data['attribute_value']
                        attribute, created = Attribute.objects.get_or_create(name=attribute_value_data['attribute'])
                        attribute_value, created = AttributeValue.objects.get_or_create(attribute=attribute,
                                                                                        value=attribute_value_data[
                                                                                            'value'])
                        ProductVariantAttribute.objects.create(variant=variant, attribute_value=attribute_value)

        return instance
