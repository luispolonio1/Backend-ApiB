from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

from .models import Red, Rio,NodoMetric,Nodo
from .serializers import RedSerializer, RioSerializer,NodoSerializer,NodoMetricWriteSerializer


@api_view(['GET', 'POST'])
def redes(request):
    if request.method == 'GET':
        redes = Red.objects.all()
        serializer = RedSerializer(redes, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = RedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET'])
def rios(request):
    if request.method == 'GET':
        rios = Rio.objects.all()
        serializer = RioSerializer(rios, many=True)
        return Response(serializer.data)
    

@api_view(['POST'])
def nodos(request):
    print(request.data)
    if request.method == 'POST':
        serializer = NodoSerializer(data=request.data)
        print(serializer.is_valid())
        print(serializer.errors)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

"""

"""


@api_view(['POST'])
def actualizar_metrica(request, nodo_id):

    nodo = get_object_or_404(Nodo, id=nodo_id)

    serializer = NodoMetricWriteSerializer(data=request.data)

    if serializer.is_valid():

        NodoMetric.objects.create(
            nodo=nodo,
            **serializer.validated_data
        )

        return Response(
            {"message": "Métrica registrada"},
            status=201
        )

    return Response(serializer.errors, status=400)