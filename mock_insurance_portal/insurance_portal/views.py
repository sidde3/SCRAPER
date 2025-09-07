from django.shortcuts import render
from .models import Patient
import random
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User


try:
    User.objects.get(username='admin')
except User.DoesNotExist:
    User.objects.create_superuser('admin', '', 'admin')

def eligibility_index(request):
    return HttpResponse("Eligibility Index Page")

def check_eligibility(patient_id):
    # Mock eligibility check, replace with actual logic
    statuses = ['eligible', 'not eligible', 'pending']
    return random.choice(statuses)

def patient_eligibility(request, patient_id):
    try:
        patient = Patient.objects.get(patient_id=patient_id)
    except Patient.DoesNotExist:
        patient = Patient.objects.create(patient_id=patient_id)
    
    eligibility_status = check_eligibility(patient_id)
    patient.eligibility_status = eligibility_status
    patient.save()

    return render(request, 'insurance_portal/eligibility.html', {
        'patient_id': patient_id,
        'eligibility_status': eligibility_status
    })

@csrf_exempt
@require_http_methods(["POST"])
def check_eligibility_with_credentials(request):
    try:
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        patient_id = data.get('patient_id')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is None:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

        # Check eligibility for the patient
        try:
            patient = Patient.objects.get(patient_id=patient_id)
            eligibility_status = patient.eligibility_status
        except Patient.DoesNotExist:
            eligibility_status = check_eligibility(patient_id)
            patient = Patient.objects.create(patient_id=patient_id, eligibility_status=eligibility_status)

        return JsonResponse({
            'patient_id': patient_id,
            'eligibility_status': eligibility_status
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)