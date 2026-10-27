from django.contrib import admin

from .models import ActividadDeportiva, Horario, Inscripcion


# Register your models here.
@admin.register(ActividadDeportiva)
class ActividadDeportivaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'lugar', 'cupo']
    search_fields = ('nombre', 'lugar')  # barra de búsqueda
    list_filter = ('lugar',)


@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ['actividad', 'dia', 'hora_inicio', 'hora_fin']
    search_fields = ('actividad__nombre', 'dia')  # barra de búsqueda
    list_filter = ('dia', 'actividad')


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ['apellido', 'nombre', 'dni', 'horario', 'estado', 'fecha_inscripcion']
    search_fields = ('apellido', 'nombre', 'dni', 'horario__actividad__nombre')  # barra de búsqueda
    list_filter = ('estado', 'fecha_inscripcion')
