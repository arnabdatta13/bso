import csv
from datetime import datetime
import os
import django

# Django setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bso.settings")
django.setup()

from app.models import Student  # Replace 'app' with your actual app name

def import_students_from_csv(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            email = row.get('Email Address', '').strip()
            phone = row.get('Phone Number', '').strip()

            # Parse date of birth
            try:
                dob = datetime.strptime(row['Date of birth'], "%d/%m/%Y").date()
            except ValueError:
                print(f"❌ Invalid date for {email or 'Unknown Email'}, skipped.")
                continue

            # Segments (optional)
            segments = []
            if 'Segments' in row and row['Segments']:
                segments = [s.strip() for s in row['Segments'].split(";")]

            # Create student — roll_number and barcode auto-generate in save()
            student = Student.objects.create(
                name=row.get('Name'),
                email=email or None,
                phone=phone or None,
                emergency_contact_number=row.get('Emergency Contact Number'),
                gender=row.get('Gender'),
                date_of_birth=dob,
                institution_name=row.get('Institution Name'),
                student_class=row.get('Class / Grade', ''),
                category=row.get('Category', ''),  
                segments=segments
            )

            print(f"✅ Added {student.name} ({student.roll_number}) with barcode")

if __name__ == "__main__":
    import_students_from_csv('data.csv')
