import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.contrib.sessions.models import Session
from rest_framework.permissions import IsAuthenticated
from users.serializers import CustomUserSerializer, AddressSerializer, PasswordChangeSerializer
from users.models import CustomUser, Address

logger = logging.getLogger('users')


class UsersListView(APIView):
    def get(self, request):
        users = CustomUserSerializer(CustomUser.objects.all(), many=True)

        return Response(users.data, status=status.HTTP_200_OK)


class SignupView(APIView):
    @staticmethod
    def post(request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():

            serializer.save()
            response_data = {
                "message": "User created successfully",
                "user": serializer.data
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        logger.error(f"Validation errors: {serializer.errors}")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():

            serializer.save(user=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Validation errors: {serializer.errors}")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            address = Address.objects.get(user=request.user, pk=pk)
        except Address.DoesNotExist:
            logger.error(f"Address not found for user {request.user}")

            return Response({'error': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = AddressSerializer(address, data=request.data, context={'user': request.user}, partial=True)
        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.error(f"Validation errors: {serializer.errors}")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    @staticmethod
    def post(request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        if not email:

            logger.error("Email is required")

            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not password:

            logger.error("Password is required")

            return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, email=email, password=password)
        if user is not None:

            login(request, user)

            return Response({"message": "Logged in successfully"}, status=status.HTTP_200_OK)

        logger.critical("Invalid credentials")

        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        logout(request)

        return Response({"message": "Logged out successfully"})


class UserProfileEditView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        user = request.user
        serializer = CustomUserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def put(request):
        user = request.user
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():

            serializer.save()
            response_data = {
                "message": "Successfully Updated the Profile",
                "Profile": serializer.data
            }

            return Response(response_data, status=status.HTTP_200_OK)
        logger.error(f"Validation errors: {serializer.errors}")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = PasswordChangeSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():

            user.set_password(serializer.validated_data['new_password'])
            user.save()
            self._invalidate_user_sessions(user)

            return Response({"message": "Password has been changed successfully."}, status=status.HTTP_200_OK)
        logger.error(f"Validation errors: {serializer.errors}")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def _invalidate_user_sessions(user):
        sessions = Session.objects.filter(expire_date__gte=timezone.now())
        for session in sessions:
            session_data = session.get_decoded()
            if user.pk == session_data.get('_auth_user_id'):
                session.delete()














