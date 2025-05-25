from django.contrib import messages
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect
from medicalregistry.models import MedicalRegistry

class OwnerOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != request.user:
            return HttpResponseNotAllowed(permitted_methods=['GET'])
        return super().dispatch(request, *args, **kwargs)


class SuccessMessageMixin:
    success_message = 'Операція успішна!'

    def form_valid(self, form):
        response = super().form_valid(form)
        return self._create_message(response)
    

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return self._create_message(response)

    def _create_message(self, response):
        messages.success(self.request, self.success_message)
        return response

class QueryFilterMixin:
    filter_param = 'completed'

    def get_queryset(self):
        qs = super().get_queryset()
        filter_value = self.request.GET.get(self.filter_param)
        if filter_value and filter_value.lower() == 'true':
            return qs.filter(completed=True)
        if filter_value and filter_value.lower() == 'false':
            return qs.filter(completed=False)
        return qs

class MedicalRegistryCounterMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = None
        if self.request.user.is_superuser:
            qs = MedicalRegistry.objects.all()
        else:
            qs = MedicalRegistry.objects.filter(user=self.request.user)

        context['total_patient'] = qs.count()
        #context['completed_money_transfers'] = qs.filter(completed=True).count()
        return context


class RedirrectOnErrorMixin:
    error_redirect_url = ...
    on_failure_message = 'Помилка при виконанні операції'

    def form_invalid(self, form):
        messages.error(self.request, self.on_failure_message)
        return redirect(self.error_redirect_url)