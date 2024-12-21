import os
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings


class CVUploadTestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="password123")
        # Obtain JWT token
        response = self.client.post(
            '/api/token/', {"username": "testuser", "password": "password123"})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        # Set up the API endpoint
        self.url = '/api/applications/'

    def test_cv_upload_success(self):
        # Create a test PDF file
        cv_file = SimpleUploadedFile(
            "test_cv.pdf", b"Dummy content", content_type="application/pdf"
        )

        # Payload with application details and the CV file
        data = {
            "company_name": "Example Corp",
            "job_title": "Software Engineer",
            "application_date": "2024-12-21",
            "status": "applied",
            "cv": cv_file,
        }

        # Perform a POST request to upload the CV
        response = self.client.post(self.url, data, format='multipart')
        print(f"Response data: {response.data}")

        # Assertions for upload
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('cv_url', response.data)

    def test_cv_upload_invalid_file_type(self):
        # Create a test non-PDF file
        invalid_file = SimpleUploadedFile(
            "test_cv.txt", b"Dummy content", content_type="text/plain")

        # Payload with invalid CV file
        data = {
            "company_name": "Example Corp",
            "job_title": "Software Engineer",
            "application_date": "2024-12-21",
            "status": "applied",
            "cv": invalid_file,
        }

        # Perform a POST request to upload the invalid CV
        response = self.client.post(self.url, data, format='multipart')

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("cv", response.data)
        self.assertEqual(
            response.data["cv"][0], "Invalid file type. Only PDF files are allowed.")

    def test_cv_upload_no_file(self):
        # Payload without the CV file
        data = {
            "company_name": "Example Corp",
            "job_title": "Software Engineer",
            "application_date": "2024-12-21",
            "status": "applied",
        }

        # Perform a POST request without a CV file
        response = self.client.post(self.url, data, format='multipart')

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.data['cv'])
