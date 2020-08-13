from .views import RegisterAPI, LoginAPI, AuthUserAPIView, UserUpdatePasswordApiView, UserDeleteApiView
from django.urls import path, include
from knox import views as knox_views

app_name = 'authapp'

urlpatterns = [
    path('register', RegisterAPI.as_view(), name='register-auth-app'),
    path('login', LoginAPI.as_view(), name='login'),
    path('logout', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall', knox_views.LogoutAllView.as_view(), name='logout-all'),
    path('user', AuthUserAPIView.as_view(), name='retrieve-user'),
    path('users/password/reset/<str:username>', UserUpdatePasswordApiView.as_view(), name='update-user-password'),
    path('users/delete/<str:username>', UserDeleteApiView.as_view(), name='delete-user'),
    path('forgot/password/reset', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
