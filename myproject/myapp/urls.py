from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="homepage"),
    path('main', views.main, name="main")
]