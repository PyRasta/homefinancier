from django.contrib import admin
from django.urls import path, include
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = [
    path('', cache_page(60)(views.index), name='screener')
]
