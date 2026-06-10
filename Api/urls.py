from django.urls import path
from .views import redes, rios, nodos,actualizar_metrica

urlpatterns = [
    path('', redes),
    path('rios/', rios),
    path('nodos/', nodos),
    path('nodos/<int:nodo_id>/metrica/',actualizar_metrica,name='actualizar_metrica'
),
]