from rest_framework import serializers
from .models import Nodo,NodoLocation,Red,Rio,NodoMetric,MotorCommand
from django.contrib.gis.geos import Point



class NodoMetricWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodoMetric
        fields = ['status', 'signal', 'bateria', 'time']


class NodoLocationWriteSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()


class NodoLocationSerializer(serializers.ModelSerializer):
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()

    class Meta:
        model = NodoLocation
        fields = ['id', 'latitude', 'longitude', 'created_at']

    def get_latitude(self, obj):
        return obj.location.y

    def get_longitude(self, obj):
        return obj.location.x


class NodoSerializer(serializers.ModelSerializer):

    ultima_metrica = serializers.SerializerMethodField()
    locations = serializers.SerializerMethodField()

    # Campos que llegan en el POST
    ultima_metrica_input = NodoMetricWriteSerializer(
        write_only=True,
        required=False
    )

    locations_input = NodoLocationWriteSerializer(
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = Nodo
        fields = [
            'id',
            'name',
            'red',
            'installed_at',
            'ultima_metrica',
            'locations',
            'ultima_metrica_input',
            'locations_input',
        ]
        read_only_fields = ['id', 'installed_at']

    def get_ultima_metrica(self, obj):
        metric = obj.metrics.order_by('-created_at').first()

        if not metric:
            return None

        return {
            'status': metric.status,
            'signal': metric.signal,
            'bateria': metric.bateria,
            'time': metric.time,
            'created_at': metric.created_at,
        }

    def get_locations(self, obj):
        location = obj.locations.order_by('-created_at').first()

        if not location:
            return []

        return [NodoLocationSerializer(location).data]

    def create(self, validated_data):

        metrica_data = validated_data.pop(
            'ultima_metrica_input',
            None
        )

        locations_data = validated_data.pop(
            'locations_input',
            []
        )

        nodo = Nodo.objects.create(**validated_data)

        if metrica_data:
            NodoMetric.objects.create(
                nodo=nodo,
                **metrica_data
            )

        for loc in locations_data:
            NodoLocation.objects.create(
                nodo=nodo,
                location=Point(
                    loc['longitude'],
                    loc['latitude']
                )
            )

        return nodo
    
class RedSerializer(serializers.ModelSerializer):

    nodos = NodoSerializer(many=True, read_only=True)

    class Meta:
        model = Red
        fields = '__all__'


class RioSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Rio
        fields = '__all__'


class MotorCommandSerializer(serializers.ModelSerializer):

    class Meta:

        model  = MotorCommand

        fields = ["id", "device_id", "action", "duration_ms", "status", "created_at"]

        read_only_fields = ["id", "status", "created_at"]