from django.urls import path, include
from django.contrib import admin
from rest_framework_simplejwt.views import TokenRefreshView
from Api.views.user_view import LoginView, RegisterView, ChangePasswordView, ValidateTokenView
from Api.views.permission_view import CustomPermissionListCreateView
from Api.views.user_permission_view import UserPermissionView, UserPermissionRemoveView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Autenticación
    path('auth/register/', RegisterView.as_view(), name="register"),
    path('auth/login/', LoginView.as_view(), name="login"),
    path('auth/validate-token/', ValidateTokenView.as_view(), name='validate_token'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('auth/refresh-token/', TokenRefreshView.as_view(), name='refresh_token'),
    # Permisos
    path("permisos/", CustomPermissionListCreateView.as_view()), 
    path('<int:idUser>/permisos/', UserPermissionView.as_view()),
    path('<int:idUser>/permisos/<int:permiso_id>/', UserPermissionRemoveView.as_view()),
]