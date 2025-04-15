"""
URL configuration for start_drf project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django_api.views import HelloView
from book.views import TestView, LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HelloView.as_view(), name='hello'),
    path('test/', TestView.as_view(), name='hello'),
    path('test/<int:book_id>/', TestView.as_view(), name='hello'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('books/', include('book.urls'))
]
