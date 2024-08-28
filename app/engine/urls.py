from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('start/', start, name='start'),
    path('auth/', auth, name='auth'),

    path('confirm/', confirm, name='confirm'),
    path('status/', status, name='status'),
]
