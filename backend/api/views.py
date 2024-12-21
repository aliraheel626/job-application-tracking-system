from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Application
from .serializers import ApplicationSerializer
from rest_framework.permissions import IsAuthenticated


class ApplicationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure only the authenticated user's applications are accessible
        return Application.objects.filter(user=self.request.user)


class ApplicationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure only the authenticated user's applications are accessible
        return Application.objects.filter(user=self.request.user)
