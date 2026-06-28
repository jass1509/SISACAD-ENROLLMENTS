import uuid
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.utils.translation import gettext_lazy as _

# Nota: Asegúrate de importar Workload y Student si están en otro archivo
# de lo contrario, puedes pasarlos como strings 'Workload' y 'Student'


def validate_even(value):
    # Nota: 'value' aquí será el ID del estudiante si se usa como validador de campo
    if value == 1:
        raise ValidationError(
            _('%(value)s is 1'),
            params={'value': value},
        )


class Inscription(models.Model):
    # Relaciones y campos (Indentados correctamente)
    workload = models.ForeignKey('Workload', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    status = models.BooleanField(default=True, null=False)
    created = models.DateTimeField(editable=False, null=False, auto_now_add=True)
    modified = models.DateTimeField(null=False, auto_now=True)

    # Subclase Meta
    class Meta:
        ordering = ['workload', 'student', 'created']
        constraints = [
            models.UniqueConstraint(fields=['workload', 'student'], name='unique_inscription')
        ]

    # Método Clean para validaciones personalizadas
    def clean(self):
        # Es una buena práctica verificar primero si los objetos existen antes de evaluar su ID
        if self.workload_id == 3 and self.student_id == 2:
            raise ValidationError("No se puede inscribir workload=3 student=2")
        super(Inscription, self).clean()

    # Método Save
    def save(self, *args, **kwargs):
        # Forzar la ejecución de clean() antes de guardar en la Base de Datos
        self.full_clean()  # Nota: full_clean() es mejor que clean() ya que ejecuta también los validators externos
        super(Inscription, self).save(*args, **kwargs)

    # Método String
    def __str__(self):
        return f"Inscripción: {self.workload} - Estudiante: {self.student}"