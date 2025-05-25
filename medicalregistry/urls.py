from django.urls import path
from medicalregistry import views

urlpatterns = [
    path('', views.MedicalRegistryListView.as_view(), name='medicalregistry_list'),
    path('create/', views.MedicalRegistryCreateView.as_view(), name='medicalregistry_create'),
    path('<int:medicalregistry_id>/delete/', views.MedicalRegistryDeleteView.as_view(), name='medicalregistry_delete'),
]