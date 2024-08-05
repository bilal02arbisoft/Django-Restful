from django.urls import path
from users.views import (SignupView, LogoutView,
                         UserProfileEditView, PasswordChangeView, AddressListCreateView,
                         AddressUpdateView, UsersListView)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/signup/', SignupView.as_view(), name='signup'),
    # path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/password_change/', PasswordChangeView.as_view(), name='password-change'),
    path('users/', UsersListView.as_view(), name='users'),
    path('profile/', UserProfileEditView.as_view(), name='profile'),
    path('address/', AddressListCreateView.as_view(), name='address'),
    path('address/<int:pk>/', AddressUpdateView.as_view(), name='address-update'),

]
