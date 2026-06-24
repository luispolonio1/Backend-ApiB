from django.urls import path
from .views import redes, rios, nodos,actualizar_metrica ,CreateCommandView, PendingCommandView,NodoLocationCreateView

urlpatterns = [
    path('', redes),
    path('rios/', rios),
    path('nodos/', nodos),
    path('nodos/<int:nodo_id>/metrica/',actualizar_metrica,name='actualizar_metrica'),
    path("motor/command/",          CreateCommandView.as_view()),
    path("motor/command/pending/",  PendingCommandView.as_view()),
    path('nodos/<int:nodo_id>/location/', NodoLocationCreateView.as_view(), name='nodo-location-create'),
]