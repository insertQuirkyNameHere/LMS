import imp
from django.urls import path
from .views import *

urlpatterns = [
    path('', DashBoard.as_view(), name='libDash')
]