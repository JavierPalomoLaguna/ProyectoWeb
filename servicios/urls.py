from django.urls import path
from . import views
from .views import procesar_reserva

urlpatterns = [
    # Página principal del restaurante
    path('', views.index_restaurante, name='index_restaurante'),
    
    # Carta del restaurante
    path('carta/', views.carta, name='carta'),
    
    # Procesar reservas
    path('reservar/', procesar_reserva, name='procesar_reserva'),
]
