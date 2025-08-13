"""
URL configuration for bso project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path("login/", views.login, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.admin_logout, name="logout"),
    path("students/", views.students, name="students"),
    path("send-sms/", views.send_sms, name="send_sms"),  # Assuming you have a view for sending SMS
    path("send-sms-all/", views.send_sms_all, name="send_sms_all"),  # New URL for sending SMS to all students
    path('scan/', views.scan_barcode_page, name='scan_page'),
    path('check-roll/', views.check_roll, name='check_roll_number'),
    path("add-student/", views.add_student, name="add-student"),  # Assuming you have a view for adding students
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
