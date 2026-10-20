from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from reservas.forms import ActividadDeportivaForm, ActividadDeportivaModificaForm
from reservas.models import ActividadDeportiva


# 1. Vista para registrar una nueva actividad deportiva (/actividades/agregar/)
def agregar_actividad(request):
    nueva_actividad = None
    if request.method == 'POST':
        actividad_form = ActividadDeportivaForm(request.POST)
        if actividad_form.is_valid():
            # Se guardan los datos que provienen del formulario en la B.D. (SQLite)
            nueva_actividad = actividad_form.save()
            messages.success(
                request,
                'Se ha agregado correctamente la Actividad Deportiva {}'.format(nueva_actividad.nombre),
            )
            actividad_form = ActividadDeportivaForm()
    else:
        actividad_form = ActividadDeportivaForm()

    return render(
        request,
        'reservas/agregar_actividad.html',
        {'form': actividad_form, 'nueva_actividad': nueva_actividad},
    )


# 2. Vista para mostrar todas las actividades deportivas (/actividades/)
def lista_actividades(request):
    actividades = ActividadDeportiva.objects.all()
    return render(request, 'reservas/lista_actividades.html', {'actividades': actividades})


# 3. Vista para mostrar los detalles de una actividad deportiva (/actividades/<int:pk>/)
def detalle_actividad(request, pk):
    actividad = get_object_or_404(ActividadDeportiva, pk=pk)
    return render(request, 'reservas/detalle_actividad.html', {'actividad': actividad})


# Vista para modificar una actividad deportiva (según teoría CRUD - Update)
def editar_actividad(request, pk):
    actividad = get_object_or_404(ActividadDeportiva, pk=pk)
    if request.method == 'POST':
        form_actividad = ActividadDeportivaModificaForm(request.POST, instance=actividad)
        if form_actividad.is_valid():
            form_actividad.save(commit=True)
            messages.success(request, 'Se ha actualizado correctamente la Actividad Deportiva')
            return redirect(reverse('reservas:detalle_actividad', args=[actividad.id]))
    else:
        form_actividad = ActividadDeportivaModificaForm(instance=actividad)

    return render(
        request,
        'reservas/agregar_actividad.html',
        {'form': form_actividad, 'editando': True, 'actividad': actividad},
    )


# Vista para eliminar una actividad deportiva (según teoría CRUD - Delete)
def eliminar_actividad(request):
    if request.method == 'POST':
        if 'id_actividad' in request.POST:
            actividad = get_object_or_404(ActividadDeportiva, pk=request.POST['id_actividad'])
            nombre_actividad = actividad.nombre
            actividad.delete()
            messages.success(
                request,
                'Se ha eliminado exitosamente la Actividad Deportiva {}'.format(nombre_actividad),
            )
        else:
            messages.error(request, 'Debe indicar qué Actividad Deportiva se desea eliminar')
    return redirect(reverse('reservas:lista_actividades'))
