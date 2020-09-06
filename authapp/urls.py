from .views import (
    RegisterAPI, LoginAPI, AuthUserAPIView, UserUpdatePasswordApiView, UserDeleteApiView, AvatarCreateAPIView,
    RatingCreateAPIView, MakeAdminMasterAPIView, MakeUserAdminAPIView, CreateDefaultAPIView, UpdateDefaultsAPIView,
    RetrieveDefaultsAPIView, DeleteAvatarModelAPIView, RetrieveAvatarAPIView, UpdateUserAPIView)
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
    path('user/update/<str:username>', UpdateUserAPIView.as_view(), name="update-user-info"),
    # Delete a user endpoint
    path('users/delete/<str:username>', UserDeleteApiView.as_view(), name='delete-user'),
    # reset users password
    path('rating/create', RatingCreateAPIView.as_view(), name="rating-create"),
    # user_type change
    path('make/', include([
        path('admin/<uuid:uuid>', MakeUserAdminAPIView.as_view(), name="make-user-admin"),
        path('master/admin/<uuid:uuid>', MakeAdminMasterAPIView.as_view(), name="make-user-master-admin")
    ])),
    # user defaults
    path('defaults/', include([
        path('create', CreateDefaultAPIView.as_view(), name="defaults-create"),
        path('update/<uuid:uuid>', UpdateDefaultsAPIView.as_view(), name="defaults-update"),
        path('retrieve/<uuid:uuid>', RetrieveDefaultsAPIView.as_view(), name="defaults-retrieve"),
    ])),
    # user avatar
    path('avatar/', include([
        path('create', AvatarCreateAPIView.as_view(), name='avatar-create'),
        path('delete/<uuid:uuid>', DeleteAvatarModelAPIView.as_view(), name="avatar-delete"),
        path('retrieve', RetrieveAvatarAPIView.as_view(), name="avatar-retrieve"),
    ]))
]
