from django.contrib.auth import login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from users.serializers import CustomUserSerializer, PasswordChangeSerializer
from django.utils import timezone
from django.contrib.sessions.models import Session


class SignupView(APIView):
    @staticmethod
    def post(request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                user_serialized = CustomUserSerializer(user)
            except ValueError as e:

                return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            response_data = {
                "message": "User created successfully",
                "user": user_serialized.data
                }

            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    @staticmethod
    def post(request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        if not email:

            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not password:

            return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, email=email, password=password)
        if user is not None:

            login(request, user)

            return Response({"message": "Logged in successfully"}, status=status.HTTP_200_OK)

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

            updated_instance = serializer.save()
            updated_serializer = CustomUserSerializer(updated_instance)
            response_data = {
                "message": "Successfully Updated the Profile",
                "Profile:": updated_serializer.data
            }

            return Response(response_data, status=status.HTTP_200_OK)

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

            return Response({"detail": "Password has been changed successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def _invalidate_user_sessions(user):
        sessions = Session.objects.filter(expire_date__gte=timezone.now())
        for session in sessions:
            session_data = session.get_decoded()
            if user.pk == session_data.get('_auth_user_id'):

                session.delete()














