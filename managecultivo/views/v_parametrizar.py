from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.contrib import messages

from ..models import Cultivo,Actividad,ActividadCultivo,Insumo,ActividadCultivoInsumo, UnidadTiempo

@login_required
# filtra la tabla
def parametrizar_cultivo(request):
    cultivo_id = request.GET.get("cultivo")  # capturamos el cultivo seleccionado
    actividades = []

    if cultivo_id:
        actividades = ActividadCultivo.objects.filter(id_cultivo = cultivo_id)

    context = {
        "cultivos": Cultivo.objects.all(),
        "actividades_lista": Actividad.objects.all(),
        "unidades": UnidadTiempo.objects.all(),
        "insumos": Insumo.objects.all(),
        "actividades": actividades,
    }
    return render(request, "parametrizar_cultivo.html", context)


@login_required
def crear_cultivo(request):
    if request.method == "POST":
        descripcion = request.POST.get("descripcion")
        tiempo_agricola = request.POST.get("tiempo_agricola")
        Cultivo.objects.create(
            descripcion=descripcion,
            tiempo_agricola=tiempo_agricola,
            registrado_por=request.user
        )
    return redirect("parametrizar_cultivo")


@login_required
def crear_actividad(request):
    if request.method == "POST":
        descripcion = request.POST.get("descripcion")
        Actividad.objects.create(
            descripcion=descripcion,
            registrado_por=request.user
        )
    return redirect("parametrizar_cultivo")

@login_required
def crear_insumo(request):
    if request.method == "POST":
        descripcion = request.POST.get("descripcion")
        cantidad_existente = request.POST.get("cantidad_existente")
        tipo = request.POST.get("tipo")

        Insumo.objects.create(
            descripcion=descripcion,
            cantidad_existente=cantidad_existente,
            tipo=tipo,
            registrado_por=request.user
        )
    return redirect("parametrizar_cultivo")


@login_required
def crear_actividadcultivo(request):
    if request.method == "POST":
        print(request.POST)  
        cultivo_id = request.POST.get("id_cultivo")
        actividad_id = request.POST.get("id_actividad")
        numero_veces = int(request.POST["numero_veces"])
        frecuencia_valor = int(request.POST["frecuencia_valor"])
        frecuencia_unidad_id = request.POST["frecuencia_unidad"]
        numero_personas = int(request.POST["numero_personas"])
        a_partir_de = int(request.POST.get("a_partir_de", 0))
        color = request.POST.get("color", "#000000")

        # 1. Crear ActividadCultivo
        act_cultivo = ActividadCultivo.objects.create(
            id_cultivo_id=cultivo_id,
            id_actividad_id=actividad_id,
            numero_veces=numero_veces,
            frecuencia_valor=frecuencia_valor,
            frecuencia_unidad_id=frecuencia_unidad_id,
            numero_personas=numero_personas,
            a_partir_de=a_partir_de,
            color=color,            
            registrado_por=request.user
        )

        # 2. Procesar insumos seleccionados
        insumos_seleccionados = request.POST.getlist("insumos")
        for insumo_id in insumos_seleccionados:
            cantidad = request.POST.get(f"cantidad_{insumo_id}")
            if cantidad:  # solo si se ingresó cantidad
                ActividadCultivoInsumo.objects.create(
                    actividad_cultivo=act_cultivo,
                    id_insumo_id=insumo_id,
                    cantidad_sugerida=cantidad,
                    registrado_por=request.user
                )
    messages.success(request, "Actividad guardada correctamente.")
    return redirect("parametrizar_cultivo")

@login_required
def borrar_actividadcultivo(request, pk):
    actividad = get_object_or_404(ActividadCultivo, pk=pk)
    actividad.delete()
    return redirect("parametrizar_cultivo")
