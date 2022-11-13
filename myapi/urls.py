from django.urls import include, path
from . import views

urlpatterns = [
    path('generate', views.generate),
    path('list', views.list),
    path('retrieve', views.retrieve)
]