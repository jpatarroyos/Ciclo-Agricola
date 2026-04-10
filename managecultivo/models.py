from django.db import models
from django.contrib.auth.models import User


# Zonas agrícolas
class ZonaAgricola(models.Model):
    id_zonaagricola = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    ubicacion = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.ubicacion}"


# Cultivo
class Cultivo(models.Model):
    id_cultivo = models.BigAutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)
    tiempo_agricola = models.IntegerField(help_text="Tiempo en días")
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.descripcion


# Actividad agrícola
class Actividad(models.Model):
    id_actividad = models.BigAutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.descripcion


# Insumos
class Insumo(models.Model):
    TIPOS = [
        ("fertilizante", "Fertilizante"),
        ("semilla", "Semilla"),
        ("herramienta", "Herramienta"),
    ]

    id_insumo = models.BigAutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)
    cantidad_existente = models.FloatField()
    tipo = models.CharField(max_length=20, choices=TIPOS, default="fertilizante")
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.descripcion} ({self.get_tipo_display()})"


class UnidadTiempo(models.Model):
    id = models.BigAutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)  # Ej: "Horas", "Días", "Semanas", "Meses"

    def __str__(self):
        return self.descripcion

# Relación Cultivo - Actividad
class ActividadCultivo(models.Model):
    id_cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE)
    id_actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    numero_veces = models.IntegerField() # Ejm 1 
    frecuencia_valor = models.IntegerField()  # Ej: Cada 8
    frecuencia_unidad = models.ForeignKey(UnidadTiempo, on_delete=models.PROTECT, related_name="frecuencias") # horas
    numero_personas = models.IntegerField()
    a_partir_de = models.IntegerField(default=0)   # días desde inicio del ciclo
    color = models.CharField(max_length=20, default="#000000")  # color en calendario
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Cultivo: {self.id_cultivo.descripcion} | Actividad: {self.id_actividad.descripcion}"


# Relación CultivoActividad - Insumos
class ActividadCultivoInsumo(models.Model):
    actividad_cultivo = models.ForeignKey(ActividadCultivo, on_delete=models.CASCADE)
    id_insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    cantidad_sugerida = models.FloatField(help_text="Cantidad requerida para la actividad")
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Cultivo: {self.actividad_cultivo.id_cultivo.descripcion} | Actividad: {self.actividad_cultivo.id_actividad.descripcion} | Insumo: {self.id_insumo.descripcion} | Cantidad: {self.cantidad_sugerida}"        

# Compra de insumos
class CompraInsumo(models.Model):
    id_insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    fecha_compra = models.DateField()
    marca = models.CharField(max_length=50)
    cantidad = models.FloatField()
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.insumo.descripcion} - {self.fecha_compra} - {self.cantidad}"


# Ciclo agrícola
class Ciclo(models.Model):
    id_ciclo = models.BigAutoField(primary_key=True)
    id_cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE)
    id_zonaagricola = models.ForeignKey(ZonaAgricola, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    cantidad_produccion = models.FloatField(help_text="Cantidad cosechada en Kg")
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Ciclo de {self.id_cultivo.descripcion} ({self.fecha_inicio} - {self.fecha_fin})"


# Personal
class Personal(models.Model):
    id_cedula = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    ROLES = [
        ("Agricultor", "Agricultor"),
        ("Fumigador", "Fumigador"),
        ("Recolector", "Recolector"),
        ("Varios", "Varios"),
    ]
    rol = models.CharField(max_length=20, choices=ROLES, default="Varios")

    def __str__(self):
        return f"{self.id_cedula} - {self.nombre} ({self.rol})"

# Actividades dentro del ciclo
class ActividadCiclo(models.Model):
    id_ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE)
    id_actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    fecha_programada = models.DateField()
    numero_personas = models.IntegerField()
    color = models.CharField(max_length=20, default="#000000")  # color en calendario    
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.id_actividad.descripcion} en {self.id_ciclo.id_cultivo.descripcion} el {self.fecha_programada}"


# Insumos utilizados en actividades dentro del ciclo
class ActividadCicloInsumo(models.Model):
    actividad_ciclo = models.ForeignKey(ActividadCiclo, on_delete=models.CASCADE)
    id_insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    cantidad_utilizada = models.FloatField(help_text="Cantidad real utilizada en Kg")
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.insumo.descripcion} usado en {self.actividad_ciclo.id_actividad.descripcion}"


# Relación Personal - Ciclo
class ActividadCicloPersonal(models.Model):
    actividad_ciclo = models.ForeignKey(ActividadCiclo, on_delete=models.CASCADE)
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.personal.nombre} en ciclo {self.actividad_ciclo.id_ciclo.id_cultivo.descripcion}"
