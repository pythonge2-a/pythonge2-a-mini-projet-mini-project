from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Page d'accueil
    path('edit/', views.edit_code, name='edit_code'),  # Page d'édition
    path('generate/', views.generate_video_view, name='generate_video'),  # Page de génération de vidéo
    path('result/', views.result , name='result'),  # Page de résultat
]
