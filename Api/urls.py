from django.urls import path
from django.contrib import admin
from Api.views.user_view import LoginView, RegisterView, ChangePasswordView, ValidateTokenView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Autenticación
    path('auth/register/', RegisterView.as_view(), name="register"),
    path('auth/login/', LoginView.as_view(), name="login"),
    path('auth/validate-token/', ValidateTokenView.as_view(), name='validate_token'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='change_password'),
]