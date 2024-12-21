from django.db import models

from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
import uuid
import os


def application_cv_upload_path(instance, filename):
    # Generate a unique UUID for the file
    unique_id = uuid.uuid4()
    # Get the file extension
    extension = os.path.splitext(filename)[1]
    # Construct the file path
    return f'applications/user_{instance.user.id}/{unique_id}/{filename}'


class Application(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('interview', 'Interview Scheduled'),
        ('offer', 'Offer Received'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='applications')
    company_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    application_date = models.DateField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='applied')
    cv = models.FileField(upload_to=application_cv_upload_path,
                          blank=True, null=True)  # CV as optional field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.job_title} at {self.company_name} ({self.get_status_display()})"
