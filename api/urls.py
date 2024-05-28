from django.urls import path
from . import views

urlpatterns = [
    path("notify_new_activity", views.get),
]
