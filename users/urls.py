from django.urls import path
from .views import UserAPI, RegisterAPI, LoginAPI
from knox import views as knox_views


from .views import EmailVerificationAPI

urlpatterns = [
    path('user', UserAPI.as_view(), name='user'),
    path('register', RegisterAPI.as_view(), name='register'),
    path('verify-email', EmailVerificationAPI),
    path('login', LoginAPI.as_view(), name='login'),
    path('logout', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall', knox_views.LogoutAllView.as_view(), name='logoutall'),
]
