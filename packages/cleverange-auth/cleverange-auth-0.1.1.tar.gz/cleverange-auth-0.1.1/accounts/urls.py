from os import name
from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterTemplateView.as_view(), name='register'),
    path('verification/<str:account_code>/', views.account_verification, name='verify'),
    path('login/', views.LoginTemplateView.as_view(), name='login'),

]
