import pytest
from django.db.utils import IntegrityError
from categories.models import Category, SubCategory


@pytest.fixture
def category():

    return Category.objects.create(name='Electronics', description='Electronic items')


@pytest.fixture
def subcategory(category):

    return SubCategory.objects.create(category=category, name='Smartphones', description='All types of smartphones')


@pytest.mark.django_db
class TestCategoryModel:
    def test_create_category(self, category):
        assert category.name == 'Electronics'
        assert category.description == 'Electronic items'

    def test_create_category_without_description(self):
        category = Category.objects.create(name='Furniture')
        assert category.name == 'Furniture'
        assert category.description is None

    def test_update_category(self, category):
        category.name = 'Gadgets'
        category.save()
        updated_category = Category.objects.get(id=category.id)
        assert updated_category.name == 'Gadgets'

    def test_delete_category(self, category):
        category_id = category.id
        category.delete()
        with pytest.raises(Category.DoesNotExist):
            Category.objects.get(id=category_id)

    def test_category_str_method(self, category):
        assert str(category) == 'Electronics'


@pytest.mark.django_db
class TestSubCategoryModel:
    def test_create_subcategory(self, subcategory):
        assert subcategory.category.name == 'Electronics'
        assert subcategory.name == 'Smartphones'
        assert subcategory.description == 'All types of smartphones'

    def test_create_subcategory_without_description(self, category):
        subcategory = SubCategory.objects.create(category=category, name='Laptops')
        assert subcategory.category == category
        assert subcategory.name == 'Laptops'
        assert subcategory.description is None

    def test_create_subcategory_without_category(self):
        with pytest.raises(IntegrityError):
            SubCategory.objects.create(name='Invalid SubCategory')

    def test_update_subcategory(self, subcategory):
        subcategory.name = 'Mobile Phones'
        subcategory.save()
        updated_subcategory = SubCategory.objects.get(id=subcategory.id)
        assert updated_subcategory.name == 'Mobile Phones'

    def test_delete_subcategory(self, subcategory):
        subcategory_id = subcategory.id
        subcategory.delete()
        with pytest.raises(SubCategory.DoesNotExist):
            SubCategory.objects.get(id=subcategory_id)

    def test_subcategory_str_method(self, subcategory):
        assert str(subcategory) == 'Smartphones'
