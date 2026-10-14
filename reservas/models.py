from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models import F, Q


# Create your models here.
class ActividadDeportiva(models.Model):
    """Actividades deportivas que ofrece la plataforma Deportes Unca."""

    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(
        max_length=500,
        help_text="Ingrese la descripción de la actividad deportiva",
    )
    lugar = models.CharField(max_length=100)
    cupo = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Cantidad máxima de participantes permitidos",
    )

    class Meta:
        verbose_name = "Actividad deportiva"
        verbose_name_plural = "Actividades deportivas"
        ordering = ["nombre"]
        constraints = [
            models.CheckConstraint(
                condition=Q(cupo__gte=1),
                name="actividad_cupo_mayor_a_cero",
            ),
        ]

    def __str__(self):
        return f"{self.nombre} ({self.lugar}) - cupo: {self.cupo}"


class Horario(models.Model):
    """Horarios disponibles para cada actividad deportiva."""

    class Dia(models.TextChoices):
        LUNES = "Lunes", "Lunes"
        MARTES = "Martes", "Martes"
        MIERCOLES = "Miercoles", "Miércoles"
        JUEVES = "Jueves", "Jueves"
        VIERNES = "Viernes", "Viernes"
        SABADO = "Sabado", "Sábado"
        DOMINGO = "Domingo", "Domingo"

    # Una actividad puede tener varios horarios; cada horario pertenece a una actividad.
    actividad = models.ForeignKey(
        ActividadDeportiva,
        on_delete=models.CASCADE,
        related_name="horarios",
    )
    dia = models.CharField(max_length=10, choices=Dia.choices)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        verbose_name = "Horario"
        verbose_name_plural = "Horarios"
        ordering = ["actividad", "dia", "hora_inicio"]
        constraints = [
            models.CheckConstraint(
                condition=Q(hora_fin__gt=F("hora_inicio")),
                name="horario_fin_posterior_al_inicio",
            ),
            models.UniqueConstraint(
                fields=["actividad", "dia", "hora_inicio"],
                name="horario_unico_por_actividad",
            ),
        ]

    def __str__(self):
        return (
            f"{self.actividad.nombre} - {self.get_dia_display()} "
            f"{self.hora_inicio:%H:%M} a {self.hora_fin:%H:%M}"
        )


class Inscripcion(models.Model):
    """Inscripción de una persona a un horario de una actividad deportiva."""

    class Estado(models.TextChoices):
        ACTIVA = "Activa", "Activa"
        CANCELADA = "Cancelada", "Cancelada"

    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(
        max_length=8,
        validators=[RegexValidator(r"^\d{7,8}$", "El DNI debe tener 7 u 8 dígitos.")],
    )
    fecha_inscripcion = models.DateField(auto_now_add=True)
    estado = models.CharField(
        max_length=10,
        choices=Estado.choices,
        default=Estado.ACTIVA,
    )
    # Cada inscripción está asociada a un horario.
    horario = models.ForeignKey(
        Horario,
        on_delete=models.CASCADE,
        related_name="inscripciones",
    )

    class Meta:
        verbose_name = "Inscripción"
        verbose_name_plural = "Inscripciones"
        ordering = ["-fecha_inscripcion", "apellido", "nombre"]
        constraints = [
            models.UniqueConstraint(
                fields=["dni", "horario"],
                name="inscripcion_unica_por_horario",
            ),
        ]

    def __str__(self):
        return f"{self.apellido}, {self.nombre} (DNI {self.dni}) - {self.estado}"
