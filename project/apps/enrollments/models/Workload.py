import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Workload(models.Model):
    # Opciones para los grupos
    GROUPS = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),
    ]

    # Opciones para los laboratorios
    LABORATORIES = [
        ('lab01', 'Laboratorio 01'),
        ('lab02', 'Laboratorio 02'),
        ('lab03', 'Laboratorio 03'),
        ('lab04', 'Laboratorio 04'),
        ('lab05', 'Laboratorio 05'),
        ('lab06', 'Laboratorio 06'),
        ('lab07', 'Laboratorio 07'),
        ('lab08', 'Laboratorio 08'),
    ]

    # Relaciones y Campos usando nombres de app explícitos ('enrollments.Modelo')
    course = models.ForeignKey('enrollments.Course', on_delete=models.CASCADE, related_name='workloads')
    teacher = models.ForeignKey('enrollments.Teacher', on_delete=models.CASCADE, related_name='workloads')

    group = models.CharField(null=False, max_length=1, choices=GROUPS, default='A')
    laboratory = models.CharField(null=False, max_length=5, choices=LABORATORIES, default='lab01')
    capacity = models.PositiveIntegerField(null=False, default=20)
    status = models.BooleanField(default=True, null=False)
    created = models.DateTimeField(editable=False, null=False, auto_now_add=True)
    modified = models.DateTimeField(null=False, auto_now=True)

    # Subclase Meta
    class Meta:
        db_table = 'workload'
        ordering = ['course', 'group', 'laboratory', 'capacity', 'teacher']
        constraints = [
            models.UniqueConstraint(fields=['course', 'group'], name='unique_workload')
        ]

    # Método String
    def __str__(self):
        return f"{self.course} - Grupo {self.group} - {self.laboratory} ({self.teacher})"