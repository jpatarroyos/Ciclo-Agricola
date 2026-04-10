from django.contrib import admin
from .models import (
    ZonaAgricola, Cultivo, Actividad, Insumo,
    ActividadCultivo, ActividadCultivoInsumo, CompraInsumo,
    Ciclo, ActividadCiclo, ActividadCicloInsumo,
    Personal, ActividadCicloPersonal, UnidadTiempo
)

admin.site.register(ZonaAgricola)
admin.site.register(Cultivo)
admin.site.register(Actividad)
admin.site.register(Insumo)
admin.site.register(ActividadCultivo)
admin.site.register(ActividadCultivoInsumo)
admin.site.register(CompraInsumo)
admin.site.register(Ciclo)
admin.site.register(Personal)
admin.site.register(ActividadCiclo)
admin.site.register(ActividadCicloInsumo)
admin.site.register(ActividadCicloPersonal)
admin.site.register(UnidadTiempo)

# Register your models here.
