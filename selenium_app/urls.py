from django.contrib import admin
from django.urls import path
from selenium_app import views

urlpatterns = [
    path("", views.result, name="result"),
]
