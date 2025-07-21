from django.urls import path
from . import views

app_name = "Customer"

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('profile/', views.Customer_Profile, name='profile')
]