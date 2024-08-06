import pytest
from django.core.exceptions import ValidationError
from users.models import CustomUser, Profile, Address
from django.db import IntegrityError


@pytest.fixture
def custom_user(db):
    user = CustomUser.objects.create_user(email='test@example.com', first_name='Test', last_name='User', password='password123')
    return user


@pytest.mark.django_db
def test_user_creation_valid_data(custom_user):
    user = custom_user
    assert user.email == 'test@example.com'
    assert user.first_name == 'Test'
    assert user.last_name == 'User'
    assert user.is_active
    assert not user.is_staff


@pytest.mark.django_db
def test_user_creation_missing_first_name():
    with pytest.raises(IntegrityError):
        CustomUser.objects.create_user(
            email='test@example.com',
            first_name=None,
            last_name='User',
            password='password123'
        )


@pytest.mark.django_db
def test_user_creation_missing_last_name():
    with pytest.raises(IntegrityError):
        CustomUser.objects.create_user(
            email='test@example.com',
            first_name='Test',
            last_name=None,
            password='password123'
        )


@pytest.mark.django_db
def test_user_creation_missing_email():

    user = CustomUser.objects.create_user(
            email='',
            first_name='Test',
            last_name='User',
            password='password123'
        )
    with pytest.raises(ValidationError):
        user.full_clean()


@pytest.mark.django_db
def test_user_creation_duplicate_email(custom_user):
    with pytest.raises(IntegrityError):
        CustomUser.objects.create_user(
            email='test@example.com',
            first_name='Test2',
            last_name='User2',
            password='password1234'
        )


@pytest.mark.django_db
def test_user_string_representation(custom_user):
    user = custom_user
    assert str(user) == 'test@example.com'


@pytest.mark.django_db
def test_user_is_active_by_default(custom_user):
    user = custom_user
    assert user.is_active


@pytest.mark.django_db
def test_user_is_not_staff_by_default(custom_user):
    user = custom_user
    assert not user.is_staff


@pytest.mark.django_db
def test_profile_creation_valid_data(custom_user):
    user = custom_user
    profile = Profile.objects.create(
        user=user,
        date_of_birth='2000-01-01',
        phone_number='12345678901',
        gender='M'
    )
    assert profile.user == user
    assert profile.date_of_birth == '2000-01-01'
    assert profile.phone_number == '12345678901'
    assert profile.gender == 'M'
    assert profile.last_updated is not None


@pytest.mark.django_db
def test_profile_creation_invalid_phone_number(custom_user):
    user = custom_user
    profile = Profile(
        user=user,
        date_of_birth='2000-01-01',
        phone_number='12345',  # Invalid phone number, less than 11 digits
        gender='M'
    )
    with pytest.raises(ValidationError):
        profile.full_clean()


@pytest.mark.django_db
def test_profile_creation_invalid_gender(custom_user):
    user = custom_user
    profile = Profile(
        user=user,
        date_of_birth='2000-01-01',
        phone_number='12345678901',
        gender='X'  # Invalid gender
    )
    with pytest.raises(ValidationError):
        profile.full_clean()


@pytest.mark.django_db
def test_profile_creation_missing_date_of_birth(custom_user):
    user = custom_user
    profile = Profile(
        user=user,
        date_of_birth=None,  # Missing date of birth
        phone_number='12345678901',
        gender='M'
    )
    with pytest.raises(ValidationError):
        profile.full_clean()


@pytest.mark.django_db
def test_create_address(custom_user):
    user = custom_user
    address = Address.objects.create(
        user=user,
        address_line_1='123 Main St',
        city='Test City',
        province='Test Province',
        country='Test Country',
        is_default=True
    )
    assert address.user == user
    assert address.address_line_1 == '123 Main St'
    assert address.city == 'Test City'
    assert address.province == 'Test Province'
    assert address.country == 'Test Country'
    assert address.is_default is True


@pytest.mark.django_db
def test_update_address(custom_user):
    user = custom_user
    address = Address.objects.create(
        user=user,
        address_line_1='123 Main St',
        city='Test City',
        province='Test Province',
        country='Test Country'
    )
    address.address_line_1 = '456 Another St'
    address.city = 'Another City'
    address.save()

    updated_address = Address.objects.get(id=address.id)
    assert updated_address.address_line_1 == '456 Another St'
    assert updated_address.city == 'Another City'


@pytest.mark.django_db
def test_address_str_representation(custom_user):
    user = custom_user
    address = Address.objects.create(
        user=user,
        address_line_1='123 Main St',
        city='Test City',
        province='Test Province',
        country='Test Country'
    )
    assert str(address) == '123 Main St, Test City'


@pytest.mark.django_db
def test_set_default_address(custom_user):
    user = custom_user
    address1 = Address.objects.create(
        user=user,
        address_line_1='123 Main St',
        city='Test City',
        province='Test Province',
        country='Test Country',
        is_default=True
    )
    address2 = Address.objects.create(
        user=user,
        address_line_1='456 Another St',
        city='Another City',
        province='Another Province',
        country='Another Country',
        is_default=False
    )

    address2.is_default = True
    address2.save()

    address1.refresh_from_db()
    address2.refresh_from_db()

    assert address1.is_default is True
    assert address2.is_default is True


@pytest.mark.django_db
def test_address_with_optional_fields(custom_user):
    user = custom_user
    address = Address.objects.create(
        user=user,
        address_line_1='123 Main St',
        address_line_2='Apt 4B',
        city='Test City',
        province='Test Province',
        country='Test Country'
    )
    assert address.address_line_2 == 'Apt 4B'
