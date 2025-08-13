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
    
@admin_login_required
def add_student(request):
    if request.method == 'POST':
        # Basic fields
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone_number')
        date_of_birth = request.POST.get('date_of_birth')

        # New fields
        student_class = request.POST.get('student_class')  # Dropdown value
        category = request.POST.get('category')            # Dropdown value
        segments = request.POST.getlist('segments')        # Checkbox values as list

        print(f"Adding student: {name}, Email: {email}, Phone: {phone}, DOB: {date_of_birth}, "
              f"Class: {student_class}, Category: {category}, Segments: {segments}")

        # Create and save student instance
        student = Student(
            name=name,
            email=email,
            phone=phone,
            date_of_birth=date_of_birth,
            student_class=student_class,
            category=category,
            segments=segments
        )
        student.save()

        messages.success(
            request,
            f"Student {name} added successfully with roll number {student.roll_number}."
        )
        return redirect('dashboard')

    return render(request, "add_student.html")


