from django.contrib import admin

# Register your models here.

from .models.Course import Course
from .models.Teacher import Teacher
from .models.Workload import Workload
from .models.Student import Student
from .models.Inscription import Inscription

admin.site.register(Course)
admin.site.register(Teacher)
admin.site.register(Workload)
admin.site.register(Student)
admin.site.register(Inscription)