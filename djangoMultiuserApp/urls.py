from django.urls import path,include
from .views import UserRegistrationView, UserProfileView, UserChangePasswordView, UserLoginView

urlpatterns = [
    # path('auth/', include('djoser.urls')),
    path('auth/register/',UserRegistrationView.as_view(),name='registration'),
    path('auth/profile/', UserProfileView.as_view(),name='profile'),
    path('auth/login/', UserLoginView.as_view(),name="login"),
    path('auth/set_password/', UserChangePasswordView.as_view(), name="set-password"),
    path('auth/', include('djoser.urls.jwt')),
]