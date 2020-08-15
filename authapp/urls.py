from .views import RegisterAPI, LoginAPI, AuthUserAPIView, UserUpdatePasswordApiView, UserDeleteApiView
from django.urls import path, include
from knox import views as knox_views

app_name = 'authapp'

urlpatterns = [
    # register a user endpoint
    path('register', RegisterAPI.as_view(), name='register-auth-app'),
    # login a user
    path('login', LoginAPI.as_view(), name='login'),
    # log out a user endpoint
    path('logout', knox_views.LogoutView.as_view(), name='logout'),
    # logout all users
    path('logoutall', knox_views.LogoutAllView.as_view(), name='logout-all'),
    # retrieve users password
    path('user', AuthUserAPIView.as_view(), name='retrieve-user'),
    # Update users password
    path('users/password/reset/<str:username>', UserUpdatePasswordApiView.as_view(), name='update-user-password'),
    # Delete a user endpoint
    path('users/delete/<str:username>', UserDeleteApiView.as_view(), name='delete-user'),
    # reset users password
    path('forgot/password/reset', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
