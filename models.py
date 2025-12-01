from django.db import models

class Solicitante(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Uso(models.Model):
    tipo = models.CharField(max_length=100)

    def __str__(self):
        return self.tipo

class Espacio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Reserva(models.Model):
    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE)
    solicitante = models.ForeignKey(Solicitante, on_delete=models.CASCADE)
    uso = models.ForeignKey(Uso, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    justificacion = models.TextField()
    imagen = models.ImageField(upload_to="eventos/", null=True, blank=True)
    estado = models.CharField(
        max_length=20,
        default="pendiente",
        choices=[
            ("pendiente", "Pendiente"),
            ("aprobado", "Aprobado"),
            ("rechazado", "Rechazado"),
        ],
    )

    def __str__(self):
        return f"Reserva {self.id} - {self.solicitante.nombre}"
