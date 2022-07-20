from django.contrib import admin
from django.urls import path, include
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = [
    path('', cache_page(60)(views.index), name='screener'),
    path('selection_country/', views.selection_country, name='selection_country'),
    path('get_stock_params/', views.get_stock_params),
    path('get_snp500/', views.get_snp500)
]
