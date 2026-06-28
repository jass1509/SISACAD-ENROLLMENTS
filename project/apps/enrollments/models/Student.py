import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class Student(models.Model):
    # Campos del modelo (Indentados con 4 espacios)
    cui = models.IntegerField(unique=True, null=True, blank=True)
    names = models.CharField(null=False, blank=False, max_length=155)
    father_surname = models.CharField(null=False, blank=False, max_length=155)
    mother_surname = models.CharField(null=False, blank=False, max_length=155)
    email = models.EmailField(unique=True, null=True, blank=True, max_length=255)
    phone = models.CharField(null=True, blank=True, max_length=255)
    status = models.BooleanField(default=True, null=False)
    created = models.DateTimeField(editable=False, null=False, auto_now_add=True)
    modified = models.DateTimeField(null=False, auto_now=True)

    # Subclase Meta
    class Meta:
        ordering = ['cui', 'names', 'father_surname', 'mother_surname']

    # Métodos del modelo
    def save(self, *args, **kwargs):
        # Validación para evitar errores si los campos llegan vacíos
        if self.names:
            self.names = self.names.upper()
        if self.father_surname:
            self.father_surname = self.father_surname.upper()
        if self.mother_surname:
            self.mother_surname = self.mother_surname.upper()
            
        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        # Formato f-string limpio para legibilidad en el administrador de Django
        return f"{self.cui} - {self.names} {self.father_surname} {self.mother_surname}".strip()