"""referral_microservice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.views import get_swagger_view
from api import views
from api.views import my_recommendations_view, request_view

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.registration_view, name='register'),
    path('', schema_view, name='docs'),
    path('profiles/<int:pk>/', my_recommendations_view, name='my_recommendations_view'),
    # path('<str:ref_code>/', home, name='home'),
    path('req/', request_view, name='request_view'),
]
