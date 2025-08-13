from django.contrib import admin
from app.models import AdminUser, Student
# Register your models here.

admin.site.register(AdminUser)
admin.site.register(Student)  # Register the Student model as well