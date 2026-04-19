from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ..models import Ciclo, CicloActividad, CicloActividadInsumo, Actividad, Insumo,Personal, CicloActividadPersonal

import calendar


def ajustar_ciclo(request, ciclo_id):

    ciclo = get_object_or_404(Ciclo, pk=ciclo_id)

    inicio_mes = ciclo.fecha_inicio.replace(day=1)
    fin_mes = ciclo.fecha_fin.replace(day=1)

    # Determinar mes actual desde querystring o usar fecha_inicio del ciclo
    mes_str = request.GET.get("mes")
    mes_str = request.GET.get("mes")
    if mes_str:
        try:
            year, month = map(int, mes_str.split("-"))
            fecha_base = datetime(year, month, 1).date()
        except ValueError:
            fecha_base = inicio_mes
    else:
        fecha_base = inicio_mes

    # Convertir a índice de meses para comparar
    inicio_index = inicio_mes.year * 12 + inicio_mes.month
    fin_index = fin_mes.year * 12 + fin_mes.month
    base_index = fecha_base.year * 12 + fecha_base.month
    print(">>> mes_str recibido:", mes_str)
    print(">>> inicio_index:", inicio_index, "fin_index:", fin_index, "base_index:", base_index)
    print(">>> fecha_base final:", fecha_base)

    if base_index < inicio_index:
        fecha_base = inicio_mes
    if base_index > fin_index:
        fecha_base = fin_mes

    # Generar calendario del mes seleccionado
    actividades_ciclo = CicloActividad.objects.filter(id_ciclo=ciclo).order_by("fecha_programada")
    cal = calendar.Calendar(firstweekday=0)
    semanas = cal.monthdatescalendar(fecha_base.year, fecha_base.month)

    calendario = []
    for semana in semanas:
        dias = []
        for dia in semana:
            acts_dia = [a for a in actividades_ciclo if a.fecha_programada == dia]
            dias.append({"fecha": dia, "actividades": acts_dia})
        calendario.append(dias)

    # Si viene parámetro fecha, filtrar actividades de ese día
    actividades_dia = CicloActividad.objects.none()
    fecha_seleccionada = None
    if "fecha" in request.GET:
        fecha_str = request.GET.get("fecha")
        try:
            fecha_seleccionada = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            actividades_dia = CicloActividad.objects.filter(
                id_ciclo=ciclo,
                fecha_programada=fecha_seleccionada)
            print(">>> fecha seleccionada:", fecha_seleccionada)
            print(">>> actividades_dia:", actividades_dia)
            
        except ValueError:
            pass

    # Manejo de POST (igual que lo tienes)
    if request.method == "POST":
        if "add_actividad" in request.POST:
            fecha_str = request.POST.get("fecha")
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            id_actividad = request.POST.get("id_actividad")
            numero_personas = request.POST.get("numero_personas")
            color = request.POST.get("color")

            CicloActividad.objects.create(
                id_ciclo=ciclo,
                id_actividad_id=id_actividad,
                fecha_programada=fecha,
                numero_personas=numero_personas,
                color=color,
                registrado_por=request.user
            )
            messages.success(request, "Actividad agregada correctamente")

        if "add_insumo" in request.POST:
            actividad_id = request.POST.get("actividad_id")
            insumo_id = request.POST.get("id_insumo")
            cantidad = request.POST.get("cantidad_utilizada")
            CicloActividadInsumo.objects.create(
                actividad_ciclo_id=actividad_id,
                id_insumo_id=insumo_id,
                cantidad_utilizada=cantidad,
                registrado_por=request.user
            )
        if "add_personal" in request.POST:
                actividad_id = request.POST.get("actividad_id")
                personal_id = request.POST.get("id_personal")
                CicloActividadPersonal.objects.create(
                    actividad_ciclo_id=actividad_id,
                    personal_id=personal_id
                )
                messages.success(request, "Personal asignado correctamente")            

        if "borrar_actividad" in request.POST:
            actividad_id = request.POST.get("actividad_id")
            actividad_ciclo = get_object_or_404(CicloActividad, pk=actividad_id)
            actividad_ciclo.delete()
            messages.success(request, "Actividad eliminada correctamente")

        return redirect("ajustar_ciclo", ciclo_id=ciclo.id_ciclo)

    return render(request, "ajustar_ciclo.html", {
        "ciclo": ciclo,
        "calendario": calendario,
        "mes_actual": fecha_base,
        "actividades_lista": Actividad.objects.all(),
        "insumos": Insumo.objects.all(),
        "actividades": actividades_dia,
        "fecha_seleccionada": fecha_seleccionada,
        "personal_lista": Personal.objects.all(),   
        "asignaciones": CicloActividadPersonal.objects.all(),        
    })
