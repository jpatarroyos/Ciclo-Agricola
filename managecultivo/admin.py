from django.contrib import admin
from .models import (
    ZonaAgricola, Cultivo, Actividad, Insumo,
    CultivoActividad, CultivoActividadInsumo, CompraInsumo,
    Ciclo, CicloActividad, CicloActividadInsumo,
    Personal, CicloActividadPersonal, UnidadTiempo
)

admin.site.register(ZonaAgricola)
admin.site.register(Cultivo)
admin.site.register(Actividad)
admin.site.register(Insumo)
admin.site.register(CultivoActividad)
admin.site.register(CultivoActividadInsumo)
admin.site.register(CompraInsumo)
admin.site.register(Ciclo)
admin.site.register(Personal)
admin.site.register(CicloActividad)
admin.site.register(CicloActividadInsumo)
admin.site.register(CicloActividadPersonal)
admin.site.register(UnidadTiempo)

# Register your models here.
