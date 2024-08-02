from rest_framework import serializers
from products.serializers import ProductVariantSerializer
from products.models import ProductVariant
from orders.models import Order, OrderItem
from users.models import CustomUser


class OrderItemSerializer(serializers.ModelSerializer):
    variant = ProductVariantSerializer(read_only=True)
    variant_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = OrderItem
        fields = ['variant', 'id', 'variant_id', 'quantity', 'unit_price', 'total_price']

    def create(self, validated_data):
        variant = validated_data.pop('variant')
        order_item = OrderItem.objects.create(variant=variant, **validated_data)
        return order_item

    def validate(self, data):

        variant_id = data.get('variant_id', None)

        product_variant = ProductVariant.objects.filter(id=variant_id)
        if not product_variant.exists():

            raise serializers.ValidationError("Invalid variant_id provided")
        return data


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'updated_at', 'status', 'total_price', 'items']

    def create(self, validated_data):
        items_data = validated_data.get('items', [])
        user = self.context['user']
        user = CustomUser.objects.get(pk=user.id)
        order = Order.objects.create(user=user)


        for item_data in items_data:
            variant = ProductVariant.objects.get(id=item_data['variant_id'])
            OrderItem.objects.create(order=order, variant=variant, **item_data)

        return order
