from django.urls import path
from .views import ApplicationListCreateView, ApplicationRetrieveUpdateDestroyView

urlpatterns = [
    # Your existing endpoints
    path('applications/', ApplicationListCreateView.as_view(),
         name='application-list-create'),
    path('applications/<int:pk>/',
         ApplicationRetrieveUpdateDestroyView.as_view(), name='application-detail'),



]
