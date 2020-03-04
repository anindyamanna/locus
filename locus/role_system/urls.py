from django.contrib import admin
from django.urls import path

from role_system.views import ResourceView

urlpatterns = [
    path('resource', ResourceView.as_view()),
]
