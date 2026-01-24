from django.contrib import admin
from .models import Doctor , Patient , Appointment , Prescription , Medicine , MedicalRecord
# from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Prescription)
admin.site.register(Medicine)
admin.site.register(MedicalRecord)
# admin.site.register(User)