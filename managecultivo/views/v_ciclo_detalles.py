from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ..models import Ciclo, CicloActividad, CultivoActividad
from django.contrib.auth.decorators import login_required
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
import calendar

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
    
@login_required
def detalle_ciclo(request, pk):
    ciclo = get_object_or_404(Ciclo, pk=pk)

    actividades_ciclo = CicloActividad.objects.filter(id_ciclo=pk)

    cal = calendar.Calendar(firstweekday=0)
    year, month = ciclo.fecha_inicio.year, ciclo.fecha_inicio.month
    semanas = cal.monthdatescalendar(year, month)

    calendario = []

    for semana in semanas:
        dias = []
        for dia in semana:

            acts_dia = [
                {
                    "id": a.pk,
                    "actividad": str(a.id_actividad),
                    "fecha": a.fecha_programada,
                    "estado": a.estado if hasattr(a, "estado") else None
                }
                for a in actividades_ciclo 
                if a.fecha_programada == dia
            ]

            dias.append({
                "fecha": dia.isoformat(),
                "actividades": acts_dia
            })

        calendario.append(dias)
    ciclo = {
        "pk": ciclo.pk,
        "cultivo": str(ciclo.id_cultivo),
        "zona": str(ciclo.id_zonaagricola),
        "inicio": ciclo.fecha_inicio,
        "fin": ciclo.fecha_fin,
    }

    data = {
        "calendario": calendario,
        "ciclo": ciclo
    }

    return JsonResponse(data)