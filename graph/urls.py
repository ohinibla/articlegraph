# -*- coding: utf-8 -*-

from django.urls import path
from . import views

app_name = 'graph'

urlpatterns = [
        path('', views.main.as_view(), name = 'main'),
        path('relations', views.Result.as_view(), name = 'result')
    ]
