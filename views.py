import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.utils import timezone

@csrf_exempt
def crear_reserva(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        uso_tipo = request.POST.get("uso")
        justificacion = request.POST.get("justificacion")
        imagen = request.FILES.get("imagen")

        solicitante = Solicitante.objects.create(nombre=nombre)
        uso, _ = Uso.objects.get_or_create(tipo=uso_tipo)
        espacio = Espacio.objects.first() or Espacio.objects.create(nombre="Principal")

        reserva = Reserva.objects.create(
            espacio=espacio,
            solicitante=solicitante,
            uso=uso,
            fecha_inicio=timezone.now(),
            fecha_fin=timezone.now(),
            justificacion=justificacion,
            imagen=imagen
        )

        return JsonResponse({"status": "ok", "id": reserva.id})

    return JsonResponse({"error": "Método no permitido"}, status=405)

def listar_reservas(request):
    estado = request.GET.get("estado", "aprobado")
    reservas = Reserva.objects.filter(estado=estado)

    data = []
    for r in reservas:
        data.append({
            "id": r.id,
            "titulo": f"Reserva #{r.id}",
            "fecha_inicio": r.fecha_inicio.isoformat(),
            "fecha_fin": r.fecha_fin.isoformat(),
            "estado": r.estado,
            "imagen_url": r.imagen.url if r.imagen else "",
            "solicitante": {"nombre": r.solicitante.nombre},
            "uso": {"tipo": r.uso.tipo},
        })

    return JsonResponse(data, safe=False)
