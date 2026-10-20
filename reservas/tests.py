from django.test import TestCase
from django.urls import resolve, reverse
from reservas import views
from reservas.models import ActividadDeportiva


class ActividadDeportivaViewsTest(TestCase):
    def setUp(self):
        self.actividad = ActividadDeportiva.objects.create(
            nombre="Fútbol 5",
            descripcion="Partidos de fútbol reducido en cancha sintética",
            lugar="Cancha Ciudad Universitaria",
            cupo=10,
        )

    def test_url_resolves_correctly(self):
        """Verifica que las URLs requeridas en el TP7 resuelvan a las vistas correctas."""
        self.assertEqual(resolve('/actividades/').func, views.lista_actividades)
        self.assertEqual(resolve('/actividades/agregar/').func, views.agregar_actividad)
        self.assertEqual(resolve(f'/actividades/{self.actividad.id}/').func, views.detalle_actividad)

    def test_home_view(self):
        """Verifica que la página principal (/) cargue correctamente."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/home.html')

    def test_lista_actividades_view(self):
        """Consigna 2: Verifica que /actividades/ muestre nombre, descripción, lugar y cupo."""
        response = self.client.get('/actividades/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservas/lista_actividades.html')
        self.assertContains(response, "Fútbol 5")
        self.assertContains(response, "Partidos de fútbol reducido en cancha sintética")
        self.assertContains(response, "Cancha Ciudad Universitaria")
        self.assertContains(response, "10")

    def test_detalle_actividad_view_existente(self):
        """Consigna 3: Verifica que /actividades/<id>/ muestre los detalles completos."""
        response = self.client.get(f'/actividades/{self.actividad.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservas/detalle_actividad.html')
        self.assertContains(response, self.actividad.nombre)
        self.assertContains(response, self.actividad.descripcion)
        self.assertContains(response, self.actividad.lugar)
        self.assertContains(response, str(self.actividad.cupo))

    def test_detalle_actividad_view_404(self):
        """Consigna 3: Verifica que si no existe la actividad devuelva respuesta HTTP 404."""
        response = self.client.get('/actividades/9999/')
        self.assertEqual(response.status_code, 404)

    def test_agregar_actividad_view_get(self):
        """Consigna 1: Verifica que GET /actividades/agregar/ muestre el formulario con csrf_token."""
        response = self.client.get('/actividades/agregar/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservas/agregar_actividad.html')
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertContains(response, 'name="nombre"')
        self.assertContains(response, 'name="descripcion"')
        self.assertContains(response, 'name="lugar"')
        self.assertContains(response, 'name="cupo"')

    def test_agregar_actividad_view_post_valido(self):
        """Consigna 1: Verifica que POST /actividades/agregar/ valide, guarde en BD y muestre confirmación."""
        datos = {
            'nombre': 'Básquet Universitario',
            'descripcion': 'Entrenamientos de básquet masculino y femenino',
            'lugar': 'Polideportivo UNCA',
            'cupo': 15,
        }
        response = self.client.post('/actividades/agregar/', data=datos)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ActividadDeportiva.objects.filter(nombre='Básquet Universitario').exists())
        self.assertContains(response, 'Se ha agregado correctamente la Actividad Deportiva Básquet Universitario')

    def test_agregar_actividad_view_post_invalido_cupo(self):
        """Consigna 1: Verifica que no guarde si los datos son inválidos (cupo <= 0)."""
        datos = {
            'nombre': 'Tenis de Mesa',
            'descripcion': 'Torneo interno',
            'lugar': 'Salón UNCA',
            'cupo': 0,
        }
        response = self.client.post('/actividades/agregar/', data=datos)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(ActividadDeportiva.objects.filter(nombre='Tenis de Mesa').exists())
        self.assertContains(response, 'errorlist')

    def test_editar_y_eliminar_actividad(self):
        """Verifica las vistas adicionales de modificación y eliminación de la teoría."""
        datos_editados = {
            'nombre': 'Fútbol 5 Nocturno',
            'descripcion': 'Partidos nocturnos',
            'lugar': 'Cancha Principal',
            'cupo': 14,
        }
        response_edit = self.client.post(
            reverse('reservas:editar_actividad', args=[self.actividad.id]),
            data=datos_editados,
            follow=True,
        )
        self.assertEqual(response_edit.status_code, 200)
        self.actividad.refresh_from_db()
        self.assertEqual(self.actividad.nombre, 'Fútbol 5 Nocturno')
        self.assertEqual(self.actividad.cupo, 14)

        response_del = self.client.post(
            reverse('reservas:eliminar_actividad'),
            data={'id_actividad': self.actividad.id},
            follow=True,
        )
        self.assertEqual(response_del.status_code, 200)
        self.assertFalse(ActividadDeportiva.objects.filter(id=self.actividad.id).exists())
