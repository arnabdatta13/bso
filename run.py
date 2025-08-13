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
            # Parse date of birth
            try:
                dob = datetime.strptime(row['Date of Birth'], "%Y-%m-%d").date()
            except ValueError:
                print(f"❌ Invalid date for {row['Email']}, skipped.")
                continue

            # Check if student already exists
            if Student.objects.filter(email=row['Email']).exists():
                print(f"⚠️ {row['Email']} already exists, skipped.")
                continue
            segments = [s.strip() for s in row["Segments"].split(";")]
            # Create student — roll_number and barcode will auto-generate in model's save()
            student = Student.objects.create(
                name=row['Name'],
                email=row['Email'],
                phone=row['Phone'],
                date_of_birth=dob,
                student_class=row.get('Class', ''),   # New field
                category=row.get('Category', ''),    # New field
                segments=segments    # New field
            )

            print(f"✅ Added {student.name} ({student.roll_number}) with barcode")

# Call the function
import_students_from_csv('data.csv')
