from django.db import models

# Create your models here.
class AdminUser(models.Model):
    full_name = models.CharField(max_length=150)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)  # You can store a hashed password

    created_at = models.DateTimeField(auto_now_add=True)  # Optional: track when created
    updated_at = models.DateTimeField(auto_now=True)     # Optional: track last update

    def __str__(self):
        return self.username

import uuid
from io import BytesIO
from django.db import models
from django.core.files import File
import barcode
from barcode.writer import ImageWriter
from datetime import datetime

class Student(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(unique=True,null=True,blank=True)
    phone = models.CharField(max_length=20,null=True,blank=True)
    date_of_birth = models.DateField()

    student_class = models.CharField(max_length=50,null=True,blank=True)  # Example: "Class 12", "Class 10"
    category = models.CharField(max_length=50,null=True,blank=True)      # Example: "Science", "Arts", "Commerce"
    segments = models.JSONField(default=list, blank=True, null=True)  # Example: ["A", "B", "C"]

    roll_number = models.CharField(max_length=30, unique=True, editable=False)
    barcode = models.ImageField(upload_to='barcodes/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.roll_number})"

    def save(self, *args, **kwargs):
        # Only generate roll number and barcode if not already set
        if not self.roll_number:
            # Create a formatted UUID-based roll number
            base_year = datetime.now().year
            unique_id = uuid.uuid4().hex[:6].upper()  # 6-char unique code
            self.roll_number = f"R{base_year}{unique_id}"  # Example: R2025A1B2C3

        if not self.barcode:
            # Generate barcode from roll number
            EAN = barcode.get_barcode_class('code128')
            ean = EAN(self.roll_number, writer=ImageWriter())

            buffer = BytesIO()
            ean.write(buffer)
            buffer.seek(0)
            self.barcode.save(f"{self.roll_number}.png", File(buffer), save=False)

        super().save(*args, **kwargs)
