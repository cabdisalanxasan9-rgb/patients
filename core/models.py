from django.db import models
from django.core.exceptions import ValidationError

# 1. Doctor Model
class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    profile_image = models.ImageField(
        upload_to='doctors/images/',  # sawirrada doctors
        blank=True,
        null=True,
        verbose_name="Profile Image"
    )

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"

# 2. Patient Model
class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)     
    description = models.TextField(blank=True, null=True)
    # stock = models.PositiveIntegerField(default=0)  # 👈 STOCK

    def __str__(self):
        return f"{self.name} ({self.quantity})"    

# 3. Appointment Model (Halkan ayaa laga xakameynayaa Booking-ka)
class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    
    # Waqtiyada la heli karo (tusaale ahaan)
    TIME_SLOTS = (
        ('08:00', '08:00 AM'),
        ('09:00', '09:00 AM'),
        ('10:00', '10:00 AM'),
        ('11:00', '11:00 AM'),
        ('01:00', '01:00 AM'),
        ('12:00', '12:00 PM'),
        ('13:00', '01:00 PM'),
        ('14:00', '02:00 PM'),
        ('15:00', '03:00 PM'),
        ('16:00', '04:00 PM'),
        ('17:00', '05:00 PM'),
        # Ku dar waqtiyo kale...
    )

    
    def __str__(self):
        return f"{self.patient.name} → {self.doctor.name} ({self.date}) at {self.TIME_SLOTS}"
    

    time = models.CharField(max_length=10, choices=TIME_SLOTS)
    status = models.CharField(max_length=20, default='Pending') # Pending, Completed, Cancelled

    class Meta:
        # Constraint-gan ayaa diidaya in laba qof isku Dhakhtar, isku Maalin iyo isku Waqti qabsadaan.
        unique_together = ('doctor', 'date', 'time')

    def __str__(self):
        return f"{self.patient} - {self.date} at {self.time}"

# 4. Prescription Model (Qoritaanka Dawada)
class Prescription(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='prescriptions', null=True, blank=True)
    diagnosis = models.TextField()
    medicines = models.TextField(help_text="Qor dawooyinka, kuna kala sooc comma (,)", blank=True, null=True)
    dosage = models.TextField(help_text="Qor dose kasta", default="")
    notes = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField()  # 👈 INTA DAWOO
   
    def __str__(self):
        return f"Prescription for {self.appointment.patient}"


class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    visit_date = models.DateTimeField(auto_now_add=True)
    
    # Vitals
    blood_pressure = models.CharField(max_length=20, help_text="tusaale: 120/80")
    heart_rate = models.CharField(max_length=10, help_text="BPM")
    temperature = models.CharField(max_length=10, help_text="°C")
    weight = models.CharField(max_length=10, help_text="kg")

    # Clinical Notes
    symptoms = models.TextField()
    diagnosis = models.TextField()
    treatment_plan = models.TextField()

    def __str__(self):
        return f"Record: {self.patient.full_name} - {self.visit_date.date()}"