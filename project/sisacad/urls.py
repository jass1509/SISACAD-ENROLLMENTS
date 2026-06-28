"""
URL configuration for sisacad project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from apps.enrollments.models import Teacher
from rest_framework.permissions import AllowAny

from apps.enrollments.views import CourseRosterViewSet, CourseViewSet
from apps.enrollments.views import WorkloadViewSet
from apps.enrollments.views import StudentViewSet
from apps.enrollments.views import InscriptionViewSet
from apps.enrollments.views import TeacherWithWorkloadsViewSet

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from django.conf import settings
from django.conf.urls.static import static
# --- Serializers ---
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "is_staff"]

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["names", "father_surname", "mother_surname", "status"]


# --- ViewSets ---
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    
# --- Routers ---
router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"teachers", TeacherViewSet)

router.register(r"courses",CourseViewSet)
router.register(r"workloads",WorkloadViewSet)
router.register(r"students",StudentViewSet)
router.register(r"inscriptions",InscriptionViewSet)
#nueva ruta para el json anidado
router.register(r'teachers-workloads', TeacherWithWorkloadsViewSet, basename='teachers-workload')
router.register(r'course-rosters', CourseRosterViewSet, basename='course-roster')


# --- URL Patterns ---
urlpatterns = [
    path('admin/', admin.site.urls),
    path('restful/', include(router.urls)),
    #path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path('restful/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('restful/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
