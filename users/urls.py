from django.urls import path
from users.views import (SignupView, LoginView, LogoutView,
                         UserProfileEditView, PasswordChangeView)

urlpatterns = [
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileEditView.as_view(), name='profile'),
    path('auth/password_change', PasswordChangeView.as_view(), name='password-change')
]
