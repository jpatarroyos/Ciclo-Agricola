from datetime import timedelta, datetime
from django.shortcuts import render, redirect
from ..models import Cultivo, Ciclo, CultivoActividad, CicloActividad, ZonaAgricola, CicloActividadInsumo

import calendar

from dateutil.relativedelta import relativedelta  # útil para meses

def sumar_tiempo(fecha_base, valor, unidad):
    if unidad.descripcion.lower() == "1 vez":
        return fecha_base + timedelta(days=valor)
    elif unidad.descripcion.lower() == "semanas":
        return fecha_base + timedelta(weeks=valor)
    elif unidad.descripcion.lower() == "horas":
        return fecha_base + timedelta(hours=valor)
    elif unidad.descripcion.lower() == "meses":
        return fecha_base + relativedelta(months=valor)
    else:
        # por defecto días
        return fecha_base + timedelta(days=valor)

def planear_ciclo(request):
    cultivos = Cultivo.objects.all()
    zonas = ZonaAgricola.objects.all()
    ciclo = None
    actividades_ciclo = []
    calendario = []

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

        actividades = CultivoActividad.objects.filter(id_cultivo=cultivo)
        for act in actividades:
            fecha_base = fecha_inicio + timedelta(days=act.dia_inicio)
            for i in range(30):
                fecha_prog = sumar_tiempo(fecha_base, i , act.frecuencia)                
                actividad_ciclo = CicloActividad.objects.create(
                    id_ciclo=ciclo,
                    id_actividad=act.id_actividad,
                    fecha_programada=fecha_prog,
                    numero_personas=act.numero_personas,
                    color=act.color
                )
                actividades_ciclo.append(actividad_ciclo)
                # insumos asociados
                insumos = act.fk_CultivoActividadInsumo1.all()
                for insumo in insumos:
                    CicloActividadInsumo.objects.create(
                        actividad_ciclo=actividad_ciclo,
                        id_insumo=insumo.id_insumo,
                        cantidad_utilizada=insumo.cantidad_sugerida,
                    )

        # Generar calendario del mes de inicio
        cal = calendar.Calendar(firstweekday=0)  # lunes
        year, month = fecha_inicio.year, fecha_inicio.month
        semanas = cal.monthdatescalendar(year, month)

        calendario = []
        for semana in semanas:
            dias = []
            for dia in semana:
                acts_dia = [a for a in actividades_ciclo if a.fecha_programada == dia]
                dias.append({"fecha": dia, "actividades": acts_dia})
            calendario.append(dias)

    return render(request, "planear_ciclo.html", {
        "cultivos": cultivos,
        "zonas": zonas,
        "ciclo": ciclo,
        "calendario": calendario
    })
