from django.urls import path, include
from users import views

urlpatterns = [
    path('signin/', views.signin, name='user-signin'),
    path('', views.signin),
    path('register/', views.register, name='user-register'),
    path('profile/', views.profile, name='user-profile'),
]
