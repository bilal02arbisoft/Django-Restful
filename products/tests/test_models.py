import pytest
from decimal import Decimal
from django.db.utils import IntegrityError
from categories.models import SubCategory, Category
from products.models import Product, Attribute, AttributeValue, ProductVariant, ProductVariantAttribute


@pytest.fixture
def category():

    return Category.objects.create(name='Electronics', description='Electronic items')


@pytest.fixture
def subcategory(category):

    return SubCategory.objects.create(category=category, name='Smartphones', description='All types of smartphones')


@pytest.fixture
def attribute():

    return Attribute.objects.create(name='Color')


@pytest.fixture
def product(subcategory):

    return Product.objects.create(
        name='iPhone 13',
        description='Latest Apple smartphone',
        price=Decimal('999.99'),
        subcategory=subcategory,
        stock=10
        )


@pytest.fixture
def variant(product):

    return ProductVariant.objects.create(
        product=product,
        sku=f"{product.id}",
        price=product.price,
        stock=product.stock
        )


@pytest.fixture
def variant_attribute(variant, attribute_value):

    return ProductVariantAttribute.objects.create(
        variant=variant,
        attribute_value=attribute_value
        )


@pytest.fixture
def attribute_value(attribute):

    return AttributeValue.objects.create(attribute=attribute, value='Red')


@pytest.mark.django_db
class TestProductModel:

    def test_create_product(self, product):
        assert product.name == 'iPhone 13'
        assert product.description == 'Latest Apple smartphone'
        assert product.price == Decimal('999.99')
        assert product.subcategory.name == 'Smartphones'
        assert product.stock == 10
        assert product.category.name == 'Electronics'

    def test_save_product_creates_default_variant(self, product):
        assert product.variants.count() == 1
        variant = product.variants.first()
        assert variant.sku == f"{product.id}-default"
        assert variant.price == product.price
        assert variant.stock == product.stock

    def test_product_str(self, product):
        assert str(product) == 'iPhone 13'


@pytest.mark.django_db
class TestAttributeModel:

    def test_create_attribute(self, attribute):
        assert attribute.name == 'Color'

    def test_attribute_str(self, attribute):
        assert str(attribute) == 'Color'


@pytest.mark.django_db
class TestAttributeValueModel:

    def test_create_attribute_value(self, attribute_value):
        assert attribute_value.attribute.name == 'Color'
        assert attribute_value.value == 'Red'

    def test_attribute_value_str(self, attribute_value):
        assert str(attribute_value) == 'Color: Red'


@pytest.mark.django_db
class TestProductVariantModel:

    def test_create_variant(self, variant):
        assert variant.product.name == 'iPhone 13'
        assert variant.sku == f"{variant.product.id}"
        assert variant.price == variant.product.price
        assert variant.stock == variant.product.stock

    def test_variant_str(self, variant):
        assert str(variant) == f"{variant.id}"


@pytest.mark.django_db
class TestProductVariantAttributeModel:

    def test_create_variant_attribute(self, variant_attribute):
        assert variant_attribute.variant.sku == f"{variant_attribute.variant.product.id}"
        assert variant_attribute.attribute_value.value == 'Red'

    def test_variant_attribute_str(self, variant_attribute):
        assert str(variant_attribute) == f"{variant_attribute.variant.sku} - {variant_attribute.attribute_value}"
