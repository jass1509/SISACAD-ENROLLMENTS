import uuid
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    CURRICULUMS = [
        (0, _('Sin Plan')),
        (2017, _('Plan 2017')),
        (2023, _('Plan 2023')),
        (2024, _('Plan 2024')),
    ]
    curriculum = models.IntegerField(null=False, choices=CURRICULUMS, default=2017)
    
    YEARS = [
        (0, _('Sin año')),
        (1, _('1er año')),
        (2, _('2do año')),
        (3, _('3er año')),
        (4, _('4to año')),
        (5, _('5to año')),
        (6, _('6to año')),
        (7, _('7mo año')),
    ]
    year = models.IntegerField(null=False, choices=YEARS, default=0)
    
    SEMESTERS = [
        (0, _('Sin semestre')),
        (1, _('I semestre')),
        (2, _('II semestre')),
        (3, _('III semestre')),
        (4, _('IV semestre')),
        (5, _('V semestre')),
        (6, _('VI semestre')),
        (7, _('VII semestre')),
        (8, _('VIII semestre')),
        (9, _('IX semestre')),
        (10, _('X semestre')),
    ]
    
    # ¡Corregido! Ahora está correctamente indentado dentro de la clase
    semester = models.IntegerField(null=False, choices=SEMESTERS, default=0)
    code = models.CharField(unique=True, null=True, blank=True, max_length=25)
    name = models.CharField(null=False, blank=False, max_length=255)
    acronym = models.CharField(null=True, blank=True, max_length=25)
    credits = models.DecimalField(null=True, blank=True, max_digits=4, decimal_places=2)
    theory_hours = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    practice_hours = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    laboratory_hours = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    laboratory = models.BooleanField(default=True, null=False)
    status = models.BooleanField(default=True, null=False)
    created = models.DateTimeField(editable=False, null=False, auto_now_add=True)
    modified = models.DateTimeField(null=False, auto_now=True)
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False)

    # Subclase Meta (Indentada dentro de Course)
    class Meta:
        ordering = ['curriculum', 'year', 'semester', 'code', 'name']

    # Métodos (Indentados dentro de Course)
    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.upper()
        if self.acronym is not None:
            self.acronym = self.acronym.upper()
        return super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.curriculum} - {self.code} - {self.name}"