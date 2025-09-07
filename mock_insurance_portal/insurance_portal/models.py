# insurance_portal/models.py
from django.db import models

class Patient(models.Model):
    patient_id = models.CharField(max_length=255, unique=True)
    eligibility_status = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.patient_id
