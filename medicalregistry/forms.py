from django import forms
from medicalregistry.models import MedicalRegistry


class MedicalRegistryForm(forms.ModelForm):
    class Meta:
        model = MedicalRegistry
        fields = ['doctor', 'patient', 'description']
