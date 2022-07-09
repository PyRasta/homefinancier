from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('screener', include('screener.urls'), name='screener'),
    path('stock_view/', views.stock_view),
    path('get_symbol/', views.get_symbol)
]