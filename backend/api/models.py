from django.db import models

from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords


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
    job_description = models.TextField(blank=True, null=True)
    application_date = models.DateField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='applied')
    notes = models.TextField(blank=True, null=True)
    job_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.job_title} at {self.company_name} ({self.get_status_display()})"
