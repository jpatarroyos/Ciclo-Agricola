from datetime import timedelta, datetime
from django.shortcuts import render, redirect
from ..models import Cultivo, Ciclo, ActividadCultivo, ActividadCiclo, ZonaAgricola


def planear_ciclo(request):
    cultivos = Cultivo.objects.all()
    zonas = ZonaAgricola.objects.all()
    ciclo = None
    actividades_ciclo = []

    if request.method == "POST":
        cultivo_id = request.POST["id_cultivo"]
        zona_id = request.POST["id_zonaagricola"]
        fecha_inicio = datetime.strptime(request.POST["fecha_inicio"], "%Y-%m-%d").date()

        cultivo = Cultivo.objects.get(pk=cultivo_id)
        fecha_fin = fecha_inicio + timedelta(days=cultivo.tiempo_agricola)

        ciclo = Ciclo.objects.create(
            id_cultivo=cultivo,
            id_zonaagricola_id=zona_id,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            cantidad_produccion=0
        )

        actividades = ActividadCultivo.objects.filter(id_cultivo=cultivo)
        for act in actividades:
            fecha_base = fecha_inicio + timedelta(days=act.a_partir_de)
            for i in range(act.numero_veces):
                fecha_prog = fecha_base + timedelta(days=i * act.frecuencia_valor)
                actividad_ciclo = ActividadCiclo.objects.create(
                    id_ciclo=ciclo,
                    id_actividad=act.id_actividad,
                    fecha_programada=fecha_prog,
                    numero_personas=act.numero_personas,
                    color=act.color
                )
                actividades_ciclo.append(actividad_ciclo)

    return render(request, "planear_ciclo.html", {
        "cultivos": cultivos,
        "zonas": zonas,
        "ciclo": ciclo,
        "actividades_ciclo": actividades_ciclo
    })
