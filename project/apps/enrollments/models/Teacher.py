import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class Teacher(models.Model):
    # Campos del modelo (Indentados con 4 espacios)
    names = models.CharField(null=False, blank=False, max_length=155)
    father_surname = models.CharField(null=False, blank=False, max_length=155)
    mother_surname = models.CharField(null=False, blank=False, max_length=155)
    email = models.EmailField(unique=True, null=True, blank=True, max_length=255)
    phone = models.CharField(null=True, blank=True, max_length=255)
    show_phone = models.BooleanField(default=False, null=False)
    status = models.BooleanField(default=True, null=False)
    created = models.DateTimeField(editable=False, null=False, auto_now_add=True)
    modified = models.DateTimeField(null=False, auto_now=True)

    # Subclase Meta (Indentada dentro de Teacher)
    class Meta:
        ordering = ['names', 'father_surname', 'mother_surname']

    # Métodos del modelo (Indentados dentro de Teacher)
    def save(self, *args, **kwargs):
        # Aseguramos que los nombres y apellidos siempre se guarden en mayúsculas
        if self.names:
            self.names = self.names.upper()
        if self.father_surname:
            self.father_surname = self.father_surname.upper()
        if self.mother_surname:
            self.mother_surname = self.mother_surname.upper()
            
        super(Teacher, self).save(*args, **kwargs)

    def __str__(self):
        # Usamos f-strings que es la forma moderna y limpia en Python
        return f"{self.names} {self.father_surname} {self.mother_surname}".strip()