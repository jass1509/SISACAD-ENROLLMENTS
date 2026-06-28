from rest_framework import serializers
from apps.enrollments.models import Course, Workload, Student, Inscription, Teacher

# ==========================================
# SERIALIZADORES BÁSICOS
# ==========================================

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['curriculum', 'year', 'semester', 'code', 'name', 'acronym']

class WorkloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workload
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['cui', 'father_surname', 'mother_surname', 'names']

class InscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscription
        fields = '__all__'

class StudentMinifiedSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['cui', 'full_name', 'email']

    def get_full_name(self, obj):
        return f"{obj.father_surname} {obj.mother_surname}, {obj.names}"

class InscriptionWithStudentSerializer(serializers.ModelSerializer):
    student = StudentMinifiedSerializer(read_only=True)

    class Meta:
        model = Inscription
        fields = ['id', 'student', 'created']

class CourseBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'code', 'name', 'acronym', 'credits']

class TeacherBaseSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = ['full_name']

    def get_full_name(self, obj):
        return f"{obj.father_surname} {obj.mother_surname}, {obj.names}"

# ==========================================
# SERIALIZADORES ANIDADOS (CORREGIDOS)
# ==========================================

class TeacherWorkloadSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    creator = serializers.SerializerMethodField() # Importación dinámica para evitar bucle

    class Meta:
        model = Workload
        fields = ['id', 'course', 'group', 'creator']

    def get_creator(self, obj):
        # Rompe el ciclo importando localmente dentro de la función
        from sisacad.urls import UserSerializer
        # Usamos el campo de usuario que tenga asignada tu base de datos en Workload, 
        # si se llama diferente a 'creator', reemplaza obj.creator por el correcto.
        if hasattr(obj, 'creator') and obj.creator:
            return UserSerializer(obj.creator, context=self.context).data
        return None

class TeacherWithWorkloadsSerializer(serializers.ModelSerializer):
    workloads = TeacherWorkloadSerializer(source='professor', many=True, read_only=True)

    class Meta:
        model = Teacher
        fields = ['id', 'names', 'father_surname', 'mother_surname', 'status', 'workloads']

class CourseWithEnrollmentsSerializer(serializers.ModelSerializer):
    matriculados = InscriptionWithStudentSerializer(source='inscriptions', many=True, read_only=True)
    teacher = TeacherBaseSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'code', 'name', 'acronym', 'credits', 'teacher', 'matriculados']

class CourseRosterSerializer(serializers.ModelSerializer):
    course = CourseBaseSerializer(read_only=True)
    teacher = TeacherBaseSerializer(read_only=True)
    enrolled_students = InscriptionWithStudentSerializer(source='academic', many=True, read_only=True)
    total_enrolled = serializers.SerializerMethodField()

    class Meta:
        model = Workload
        fields = [
            'id', 'course', 'group', 'laboratory', 'capacity',
            'total_enrolled', 'teacher', 'enrolled_students'
        ]

    def get_total_enrolled(self, obj):
        return obj.academic.filter(status=True).count()