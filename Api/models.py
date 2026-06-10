from django.contrib.gis.db import models






class Rio(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Red(models.Model):
    name = models.CharField(max_length=255)

    rio = models.ForeignKey(
        Rio,
        on_delete=models.CASCADE,
        related_name='redes'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    sync_seconds = models.IntegerField(default=60)

    def __str__(self):
        return self.name


class Nodo(models.Model):
    name = models.CharField(max_length=255)

    red = models.ForeignKey(
        Red,
        on_delete=models.CASCADE,
        related_name='nodos'
    )

    installed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class NodoMetric(models.Model):
    nodo = models.ForeignKey(
        Nodo,
        on_delete=models.CASCADE,
        related_name='metrics'
    )
    time = models.DecimalField(max_digits=4,decimal_places=2,default=0.00)

    status = models.BooleanField()

    signal = models.IntegerField()

    bateria = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)



class NodoLocation(models.Model):
    nodo = models.ForeignKey(
        Nodo,
        on_delete=models.CASCADE,
        related_name='locations'
    )

    location = models.PointField()

    created_at = models.DateTimeField(auto_now_add=True)