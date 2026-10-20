from django.urls import path
from reservas import views

app_name = 'reservas'

urlpatterns = [
    path('', views.lista_actividades, name='lista_actividades'),
    path('agregar/', views.agregar_actividad, name='agregar_actividad'),
    path('<int:pk>/', views.detalle_actividad, name='detalle_actividad'),
    path('editar/<int:pk>/', views.editar_actividad, name='editar_actividad'),
    path('eliminar/', views.eliminar_actividad, name='eliminar_actividad'),
]
