from rest_framework import serializers
from users.models import CustomUser, Profile, Address
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['phone_number', 'date_of_birth', 'gender']


class CustomUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'password', 'profile']
        extra_kwargs = {'password': {'write_only': True}}

    @staticmethod
    def validate_email(value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    @staticmethod
    def validate_password(value):
        validate_password(value)
        return value

    def validate(self, data):
        password = data.get('password')
        first_name = data.get('first_name')
        email = data.get('email')
        if password and first_name and password == first_name:
            raise serializers.ValidationError("Password and username cannot be the same.")

        if password and email and password == email:
            raise serializers.ValidationError("Password and email cannot be the same.")

        return data

    def create(self, validated_data):

        profile_data = validated_data.pop('profile')
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        Profile.objects.create(user=user, **profile_data)

        return user

    def update(self, instance, validated_data):
        if 'first_name' in validated_data:

            if check_password(validated_data['first_name'], instance.password):

                raise serializers.ValidationError("First name cannot be the same as the password.")
        if 'email' in validated_data:

            if check_password(validated_data['email'], instance.password):
                raise serializers.ValidationError(" Email cannot be the same as the password.")

        profile_data = {
            'phone_number': validated_data.pop('phone_number', None),
            'date_of_birth': validated_data.pop('date_of_birth', None),
            'gender': validated_data.pop('gender', None)
        }

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile = instance.profile
        profile.phone_number = profile_data.get('phone_number', profile.phone_number)
        profile.date_of_birth = profile_data.get('date_of_birth', profile.date_of_birth)
        profile.gender = profile_data.get('gender', profile.gender)
        profile.save()

        return instance


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ['id', 'address_line_1', 'address_line_2', 'city', 'province',
                  'country', 'is_default']
        read_only_fields = ['id']

    def update(self, instance, validated_data):

        instance.address_line_1 = validated_data.get('address_line_1', instance.address_line_1)
        instance.address_line_2 = validated_data.get('address_line_2', instance.address_line_2)
        instance.city = validated_data.get('city', instance.city)
        instance.province = validated_data.get('province', instance.province)
        instance.country = validated_data.get('country', instance.country)
        instance.is_default = validated_data.get('is_default', instance.is_default)
        instance.save()

        return instance


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    @staticmethod
    def validate_new_password(value):
        validate_password(value)

        return value

    def validate(self, data):
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        user = self.context.get('user')

        if not user.check_password(old_password):

            raise serializers.ValidationError("Old password is incorrect.")
        if new_password == user.email:

            raise serializers.ValidationError("New password cannot be the same as the email.")
        if new_password == user.first_name:

            raise serializers.ValidationError("New password cannot be the same as the first name.")
        if user.check_password(new_password):

            raise serializers.ValidationError("Pls use different password.")

        return data




