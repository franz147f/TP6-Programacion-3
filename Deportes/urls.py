"""
URL configuration for Deportes project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('actividades/', include('reservas.urls', namespace='reservas')),
    path('', include('usuario.urls', namespace='usuario')),
    path('', TemplateView.as_view(template_name='base/home.html'), name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
