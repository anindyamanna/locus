from django.contrib import admin
from django.urls import path

from role_system.views import CheckAccess

urlpatterns = [
    path('check-access/<resource_id>/<action_id>', CheckAccess.as_view()),
]
