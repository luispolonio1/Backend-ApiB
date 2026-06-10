from django.contrib import admin
from .models import Nodo, NodoLocation, NodoMetric, Red, Rio


admin.site.register(Nodo)
admin.site.register(NodoLocation)
admin.site.register(NodoMetric)
admin.site.register(Red)
admin.site.register(Rio)