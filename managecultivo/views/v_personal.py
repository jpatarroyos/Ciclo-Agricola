from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Personal

@login_required
def crear_personal(request):
    personas = Personal.objects.all()

    # Crear personal
    if request.method == "POST" and "crear_personal" in request.POST:
        id_cedula = request.POST.get("id_cedula")
        nombre = request.POST.get("nombre")
        telefono = request.POST.get("telefono")
        email = request.POST.get("email")
        rol = request.POST.get("rol")

        Personal.objects.create(
            id_cedula=id_cedula,
            nombre=nombre,
            telefono=telefono,
            email=email,
            rol=rol
        )
        return redirect("crear_personal")

    # Editar personal
    if request.method == "POST" and "editar_personal" in request.POST:
        persona_id = request.POST.get("persona_id")
        nombre = request.POST.get("nombre")
        telefono = request.POST.get("telefono")
        email = request.POST.get("email")
        rol = request.POST.get("rol")

        persona = get_object_or_404(Personal, pk=persona_id)
        persona.nombre = nombre
        persona.telefono = telefono
        persona.email = email
        persona.rol = rol
        persona.save()
        return redirect("crear_personal")

    return render(request, "crear_personal.html", {"personas": personas})
