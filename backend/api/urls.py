from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.urls import path
from .views import ApplicationListCreateView, ApplicationRetrieveUpdateDestroyView

urlpatterns = [
    # Your existing endpoints
    path('applications/', ApplicationListCreateView.as_view(),
         name='application-list-create'),
    path('applications/<int:pk>/',
         ApplicationRetrieveUpdateDestroyView.as_view(), name='application-detail'),

    # DRF Spectacular schema and UI views
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

]
