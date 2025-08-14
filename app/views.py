from django.shortcuts import render,redirect
from django.contrib import messages
from app.models import AdminUser,Student
from app.decorators import admin_login_required
from datetime import date
import requests

# Create your views here.
def home(request):
    if request.method == 'POST':
        roll_number = request.POST.get('roll_number')
        
        dob = request.POST.get('date_of_birth')
        print(f"Received Roll Number: {roll_number}, Date of Birth: {dob}")
        # Filter student
        student = Student.objects.filter(roll_number=roll_number, date_of_birth=dob).first()

        if student:
            return JsonResponse({
                'success': True,
                'message': 'Student found',
                'data': {
                    'name': student.name,
                    'email': student.email,
                    'phone': student.phone,
                    'roll_number': student.roll_number,
                    'class': student.student_class,
                    'category': student.category,
                    'segments': student.segments,
                    'barcode_url': student.barcode.url if student.barcode else None,
                    'dob': student.date_of_birth.strftime('%d-%m-%Y'),
                }
            })
        else:
            return JsonResponse({'success': False, 'message': 'No matching student found'}, status=404)

    return render(request, 'home.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Attempting login with username: {username} and password: {password}")  # Debugging line
        try:
            user = AdminUser.objects.get(username=username, password=password)
            # Save user ID in session
            request.session['admin_user_id'] = user.id  
            return redirect('dashboard')  # Redirect to dashboard after login
        except AdminUser.DoesNotExist:
            messages.error(request, "Invalid username or password!")
    
    return render(request, 'login.html') 


@admin_login_required
def dashboard(request):
    students = Student.objects.all()  # Fetch all students
    context = {
        'students': students
    }
    return render(request, "dashboard.html", context)

def admin_logout(request):
    request.session.flush()  # Clear all session data
    return redirect('login')

@admin_login_required
def students(request):
    return render(request, "students.html")

@admin_login_required
def send_sms(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        message = request.POST.get('message')
        print(f"Sending SMS to student ID: {student_id} with message: {message}")
        student = Student.objects.get(id=student_id)
        phone_number = student.phone
        api_key = "vc06DvQeuSOHnHwKaZaY"
        sender_id = "8809617624694"
        message = message

        # Receiver number (replace with actual number)
        receiver_number =phone_number  # Example: 01712345678

        # API URL
        url = f"http://bulksmsbd.net/api/smsapi?api_key={api_key}&type=text&number={receiver_number}&senderid={sender_id}&message={message}"

        # Send GET request
        response = requests.get(url)

        # Print response
        print(response.status_code)
        print(response.text)
    return redirect('dashboard')  # Redirect to dashboard after sending SMS

@admin_login_required
def send_sms_all(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        print(f"Sending SMS to all students with message: {message}")
        students = Student.objects.all()
        api_key = "vc06DvQeuSOHnHwKaZaY"
        sender_id = "8809617624694"

        for student in students:
            phone_number = student.phone
            receiver_number = phone_number  # Example: 01712345678
            # API URL
            url = f"http://bulksmsbd.net/api/smsapi?api_key={api_key}&type=text&number={receiver_number}&senderid={sender_id}&message={message}"
            # Send GET request
            response = requests.get(url)
            # Print response
            print(f"SMS sent to {student.name} ({receiver_number}): {response.status_code} - {response.text}")
        return redirect('dashboard')  # Redirect to dashboard after sending SMS to all
    return redirect('dashboard')  # Redirect to dashboard after sending SMS to all

@admin_login_required
def scan_barcode_page(request):
    return render(request, "scan_barcode.html")


from django.http import JsonResponse
@admin_login_required
def check_roll(request):
    roll = request.GET.get("roll")
    print(f"Checking roll number: {roll}")
    student = Student.objects.filter(roll_number=roll).first()
    if student:
        return JsonResponse({
            "exists": True,
            "name": student.name,
            "email": student.email,
            "roll": student.roll_number,
        })
    else:
        return JsonResponse({"exists": False})
    
# views.py
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from .models import Student

from datetime import datetime
from django.contrib import messages
from django.db import IntegrityError, transaction
from django.shortcuts import render, redirect

@admin_login_required
def add_student(request):
    if request.method == 'POST':
        # Required fields from the form
        name = (request.POST.get('name') or '').strip()
        email = (request.POST.get('email') or '').strip()
        date_of_birth_str = (request.POST.get('date_of_birth') or '').strip()
        gender = (request.POST.get('gender') or '').strip()
        phone = (request.POST.get('phone') or '').strip()  # <-- matches input name="phone"
        emergency_contact_number = (request.POST.get('emergency_contact_number') or '').strip()
        institution_name = (request.POST.get('institution_name') or '').strip()
        student_class = (request.POST.get('student_class') or '').strip()
        print(f"Adding student: {name}, Email: {email}, DOB: {date_of_birth_str}, {gender}, Phone: {phone}, Emergency Contact: {emergency_contact_number}, Institution: {institution_name}, Class: {student_class}")

        

        student = Student.objects.create(
            name=name,
            email=email,
            phone=phone,
            emergency_contact_number=emergency_contact_number,
            gender=gender,
            institution_name=institution_name,
            student_class=student_class,     # e.g., "Class 1" .. "Class 12" / "HSC or equivalent" / "Admission candidate"
        # optional list for JSONField
        )
        
        messages.success(request, f"Student {student.name or student.email} added successfully with roll number {student.roll_number}.")
        return redirect('dashboard')

    return render(request, "add_student.html")
