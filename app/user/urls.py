from django.urls import path

from user import views


app_name = 'user'

urlpatterns = [
    path('', views.UsersListApiView.as_view(), name='users'),
    path('register/', views.UserRegisterApiView.as_view(), name='register'),
    path('login/', views.UserLoginApiView.as_view(), name='login'),
    path('verify/', views.VerifyOtpApiView.as_view(), name='verify'),
]
