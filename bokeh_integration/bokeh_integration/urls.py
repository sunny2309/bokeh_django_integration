from django.contrib import admin
from django.urls import path, include
from stock_dashboard import views

urlpatterns = [
    path("", views.index, name="home"),
    path("stock/", include("stock_dashboard.urls")),
]
