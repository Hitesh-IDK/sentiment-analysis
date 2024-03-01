
from django.contrib import admin
from django.urls import path
from django.urls import include
from selenium_app import views

urlpatterns = [
    path("", views.index, name="Index"),
    path("result/", include("selenium_app.urls")),
    path("admin/", admin.site.urls),
]
