from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from medicalregistry.models import MedicalRegistry
from medicalregistry.forms import MedicalRegistryForm
from medicalregistry.mixins import (OwnerOnlyMixin, SuccessMessageMixin, QueryFilterMixin, 
                          MedicalRegistryCounterMixin, RedirrectOnErrorMixin)

class MedicalRegistryListView(LoginRequiredMixin, QueryFilterMixin, MedicalRegistryCounterMixin, ListView):
    model = MedicalRegistry
    template_name = 'MedicalRegistry/medicalregistry_list.html'
    context_object_name = 'medicalregistry'

    def get_queryset(self):
        medicalregistry = super().get_queryset()
        if self.request.user.is_superuser:
            return medicalregistry
        return medicalregistry
        #return money_transfers.filter(userfrom=self.request.user)

class MedicalRegistryCreateView(LoginRequiredMixin, SuccessMessageMixin, RedirrectOnErrorMixin, CreateView):
    model = MedicalRegistry
    form_class = MedicalRegistryForm
    template_name = 'medicalregistry/create_medicalregistry.html'
    success_url = reverse_lazy('medicalregistry_list')
    success_message = 'Призначено!'
    error_redirect_url = reverse_lazy('medicalregistry_list')

    def form_valid(self, form):
        form.instance.userfrom = self.request.user
        return super().form_valid(form)

class MedicalRegistryDeleteView(LoginRequiredMixin, OwnerOnlyMixin, SuccessMessageMixin, DeleteView):
    model = MedicalRegistry
    template_name = 'medicalregistry/confirm_delete.html'
    success_url = reverse_lazy('medicalregistry_list')
    pk_url_kwarg = 'medicalregistry_id'
    success_message = 'Видалено успішно!'