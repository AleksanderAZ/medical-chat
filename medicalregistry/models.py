from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class MedicalRegistry(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='edicalregistry_sent')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='edicalregistry_received')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk and 'request' in kwargs:
            self.userfrom = kwargs.pop('request').user
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.description