from rest_framework import serializers
from categories.models import Category, SubCategory


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    subcategories = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='subcategory-detail'
    )

    class Meta:
        model = Category
        fields = ['url', 'id', 'name', 'description', 'subcategories']


class SubCategorySerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.HyperlinkedRelatedField(
        view_name='category-detail',
        read_only=True
    )

    class Meta:
        model = SubCategory
        fields = ['url', 'id', 'name', 'description', 'category']

    def create(self, validated_data):
        subcategory = SubCategory.objects.create(category=self.context['category'], **validated_data)

        return subcategory
