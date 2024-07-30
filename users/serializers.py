from rest_framework import serializers
from users.models import CustomUser, Profile
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date']


class CustomUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)

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
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(password=password, **validated_data)

        return user

    def update(self, instance, validated_data):
        if 'first_name' in validated_data:

            if check_password(validated_data['first_name'], instance.password):

                raise serializers.ValidationError("First name cannot be the same as the password.")
        if 'email' in validated_data:

            if check_password(validated_data['email'], instance.password):
                raise serializers.ValidationError(" Email cannot be the same as the password.")

        profile_data = validated_data.pop('profile', None)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        if profile_data:

            profile = instance.profile
            profile.bio = profile_data.get('bio', profile.bio)
            profile.location = profile_data.get('location', profile.location)
            profile.save()

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




