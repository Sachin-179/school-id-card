from django.db import models


class Student(models.Model):
    SESSION_CHOICES = (
        ("2023-2023", "2023-2024"),
        ("2023-2024", "2023-2025"),
        ("2023-2025", "2023-2026"),
    )
    name = models.CharField(max_length=100)
    dob = models.DateField()
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=10)
    standard = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='profile_pics/',)

    admission = models.CharField(max_length=10)
    session = models.CharField(max_length=10, choices=SESSION_CHOICES)

    def __str__(self):
        return f"{self.name}-{self.father_name}"

