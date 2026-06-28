from django.shortcuts import render



from rest_framework import viewsets
from apps.enrollments.models import Course as CourseModel
from apps.enrollments.models import Workload as WorkloadModel
from apps.enrollments.models import Student as StudentModel
from apps.enrollments.models import Inscription as InscriptionModel
from apps.enrollments.models import Teacher as TeacherModel

from rest_framework.permissions import AllowAny

from apps.enrollments.serializers import CourseSerializer, TeacherWithWorkloadsSerializer
from apps.enrollments.serializers import WorkloadSerializer
from apps.enrollments.serializers import StudentSerializer
from apps.enrollments.serializers import InscriptionSerializer
# Create your views here.
# --- Course ViewSet ---
class CourseViewSet(viewsets.ModelViewSet):
    # Optimizamos la consulta cargando el creador de antemano
    queryset = CourseModel.objects.select_related('creator').all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        # El campo 'creator' del modelo recibe al usuario autenticado de la petición
        serializer.save(creator=self.request.user)


# --- Workload ViewSet ---
class WorkloadViewSet(viewsets.ModelViewSet):
    queryset = WorkloadModel.objects.all()
    serializer_class = WorkloadSerializer


# --- Student ViewSet ---
class StudentViewSet(viewsets.ModelViewSet):
    queryset = StudentModel.objects.all()
    serializer_class = StudentSerializer


# --- Inscription ViewSet ---
class InscriptionViewSet(viewsets.ModelViewSet):
    queryset = InscriptionModel.objects.all()
    serializer_class = InscriptionSerializer

class TeacherWithWorkloadsViewSet(viewsets.ModelViewSet):
    queryset = TeacherModel.objects.all().prefetch_related('professor__course', 'professor__creator')
    serializer_class = TeacherWithWorkloadsSerializer
    permission_classes = [AllowAny] 




#codigo añadido 

from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Workload
from .serializers import CourseRosterSerializer

class CourseRosterViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint para ver los cursos (cargas académicas) con sus listas de alumnos inscritos.
    Se puede filtrar un curso específico por URL: ?course_id=UUID_DEL_CURSO
    """
    serializer_class = CourseRosterSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Optimizamos la consulta con select_related y prefetch_related
        # Esto previene el problema N+1 al traer los alumnos de golpe
        queryset = Workload.objects.select_related(
            'course', 
            'teacher'
        ).prefetch_related(
            'academic__student'
        ).filter(status=True)

        # Filtro opcional por si se desea buscar solo un curso por su ID (UUID)
        course_id = self.request.query_params.get('course_id', None)
        if course_id:
            # CORREGIDO: Usar 'course_id' o 'course__id' dependiendo de cómo esté tu modelo.
            # Comúnmente en Django, si 'course' es una llave foránea, puedes filtrar directo por 'course_id'
            queryset = queryset.filter(course_id=course_id)

        return queryset