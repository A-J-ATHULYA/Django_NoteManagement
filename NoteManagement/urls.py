"""
URL configuration for NoteManagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from notes_app import views

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # User Registration
    path('api/register/', views.RegisterView.as_view()),

    # User Login (Token Authentication)
    path('api/login/', obtain_auth_token),

    # User Logout
    path('api/logout/', views.LogoutView.as_view()),

    # Delete User Account
    path('user/delete/', views.UserDeleteView.as_view()),

    # Notes List and Create
    path('api/notes/', views.NotesListCreateView.as_view()),

    # Retrieve, Update and Delete Particular Note
    path('api/notes/<int:pk>/', views.NotesDetailView.as_view()),

    # JWT Login
    path('api/jwt_login/', TokenObtainPairView.as_view()),

    # JWT Refresh Token
    path('api/token/refresh/', TokenRefreshView.as_view()),
    
    path('api/tasks/', views.TaskListCreateView.as_view()),
    
    path('api/tasks/<int:pk>/', views.TasksDetailView.as_view()), 
    
    path('api/jwt_logout/', views.JWT_LogoutView.as_view())
]
