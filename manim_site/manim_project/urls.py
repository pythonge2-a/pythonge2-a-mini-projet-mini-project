from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Page d'accueil
    path('edit/', views.edit_code, name='edit_code'),  # Page d'édition
]
