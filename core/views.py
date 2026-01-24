from sqlite3 import IntegrityError
from urllib import response
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import DoctorForm
from .models import Doctor

from .forms import AppointmentForm, PatientForm, PrescriptionForm, SignUpForm , LoginForm , MedicineForm
from .models import Doctor, Medicine, Patient, Appointment, Prescription
from datetime import date
from django.contrib.auth import login , logout
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from datetime import date
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth.decorators import login_required
from datetime import date
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import MedicalRecord
from .forms import MedicalRecordForm
from django.contrib import messages
from django.db import transaction



def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'logout.html')    



def signup_view(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('patient_list')
        else:
            print(form.errors)
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('patient_list')

    return render(request, 'login.html', {
        'form': form
    })



# ---------------- PATIENT VIEWS ----------------
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})




def patient_create(request):
    form = PatientForm(request.POST or None)
    if form.is_valid():
       form.save()
       return redirect('patient_list')
    return render(request, 'patient_list.html', {'form': form})




def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    appointments = Appointment.objects.filter(patient=patient)
    return render(request, 'patient_detail.html', {
    'patient': patient,
    'appointments': appointments
})


# ---------------- APPOINTMENT VIEWS ----------------
def appointment_list(request):
    appointments = Appointment.objects.select_related('doctor', 'patient').prefetch_related('prescription')
    return render(request, 'appointment_list.html', {'appointments': appointments})



def appointment_create(request):
    error = None
    form = AppointmentForm(request.POST or None)

    if form.is_valid():
        try:
            form.save()
            return redirect('appointment_list')
        except IntegrityError:
            error = "Dhakhtarkan waqtigan hore ayaa loo qabsaday"

    return render(request, 'appointment_form.html', {
        'form': form,
        'error': error
    })


# ---------------- PRESCRIPTION VIEWS ----------------  
def prescription_create(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == "POST":
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            medicine = form.cleaned_data['medicine']
            quantity = form.cleaned_data['quantity']

            # 1️⃣ Hubi stock (quantity field in Medicine model)
            if medicine.quantity < quantity:
                messages.error(request, "Stock-ga daawada kuma filna")
                return render(request, 'prescription_form.html', {
                    'form': form,
                    'appointment': appointment,
                })

            # 2️⃣ Save prescription + dhimista stock
            with transaction.atomic():
                prescription = form.save(commit=False)
                prescription.appointment = appointment  # 🔴 muhiim - automatically set
                prescription.save()

                # Update medicine stock
                medicine.quantity -= quantity
                medicine.save()

            messages.success(
                request,
                "Prescription waa la keydiyay, stock-gana waa la cusbooneysiiyay"
            )
            return redirect('appointment_list')

    else:
        form = PrescriptionForm()

    return render(request, 'prescription_form.html', {
        'form': form,
        'appointment': appointment,  # 🔴 template-ka u baahan
    })





@login_required
def dashbord(request):
    # 1. Tirada guud ee bukaanada
    patients_count = Patient.objects.count()

    query = request.GET.get('q') # Halkan ayuu qoraalku ka soo gelayaa
    
    # Get all today's appointments first (for stats) - before filtering
    all_today_appointments = Appointment.objects.filter(date=date.today())
    
    # 3. Xisaabinta ballamaha maanta (Status-kooda) - calculate before filtering
    total_today = all_today_appointments.count()
    pending_count = all_today_appointments.filter(status='Pending').count()
    completed_count = all_today_appointments.filter(status='Completed').count()
    cancelled_count = all_today_appointments.filter(status='Cancelled').count()
    
    # Now filter for display (with search query if provided)
    today_appointments = all_today_appointments.select_related('patient', 'doctor', 'prescription')
    
    # Haddii uu jiro qoraal la raadinayo
    if query:
        today_appointments = today_appointments.filter(
            Q(patient__first_name__icontains=query) | 
            Q(patient__last_name__icontains=query) |
            Q(doctor__first_name__icontains=query) |
            Q(doctor__last_name__icontains=query)
        )
    
    # 4. Xogta kale (Optional)
    medicines_count = Medicine.objects.count()
    
    # Calculate percentages for progress bars
    pending_percent = (pending_count / total_today * 100) if total_today > 0 else 0
    completed_percent = (completed_count / total_today * 100) if total_today > 0 else 0
    cancelled_percent = (cancelled_count / total_today * 100) if total_today > 0 else 0
    
    context = {
        'patients_count': patients_count,
        'today_appointments': today_appointments,
        'pending_count': pending_count,
        'completed_count': completed_count,
        'cancelled_count': cancelled_count,
        'medicines_count': medicines_count,
        'total_today': total_today,
        'pending_percent': round(pending_percent, 1),
        'completed_percent': round(completed_percent, 1),
        'cancelled_percent': round(cancelled_percent, 1),
    }
    
    return render(request, 'dashbord.html', context)


# -------- UPDATE & DELETE --------
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    form = PatientForm(request.POST or None, instance=patient)
    if form.is_valid():
       form.save()
       return redirect('patient_list')
    return render(request, 'patient_form.html', {'form': form})




def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
       patient.delete()
       return redirect('patient_list')
    return render(request, 'patient_confirm_delete.html', {'patient': patient})




def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    appointments = Appointment.objects.filter(patient=patient)
    return render(request, 'patient_detail.html')



def patient_create(request):
    form = PatientForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('patient_list')
    return render(request, 'patient_form.html', {'form': form})



def create_prescription(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Haddii prescription hore u jiro, update samee
    prescription, created = Prescription.objects.get_or_create(appointment=appointment)

    if request.method == 'POST':
        form = PrescriptionForm(request.POST, instance=prescription)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')  # ama dashboard
    else:
        form = PrescriptionForm(instance=prescription)

    return render(request, 'prescription.html', {
        'form': form,
        'appointment': appointment
    })



def prescription_list(request):
    prescriptions = Prescription.objects.all()
    return render(request, 'prescription_list.html', {'prescriptions': prescriptions})




def medicine_list(request):
    medicines = Medicine.objects.all()
    return render(request, 'medicine_list.html', {'medicines': medicines})

# Faahfaahinta dawo
def medicine_detail(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    return render(request, 'medicine_detail.html', {'medicine': medicine})

# Ku dar dawo cusub
def medicine_add(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medicine_list')
    else:
        form = MedicineForm()
    return render(request, 'medicine_form.html', {'form': form})

# Edit / Update
def medicine_edit(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            return redirect('medicine_list')
    else:
        form = MedicineForm(instance=medicine)
    return render(request, 'medicine_form.html', {'form': form})

# Delete
def medicine_delete(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        medicine.delete()
        return redirect('medicine_list')
    return render(request, 'medicine_confirm_delete.html', {'medicine': medicine})





def patient_report(request , pk):
    patient = Patient.objects.get(patient , pk=pk)
    appointments = Appointment.objects.filter(patient=patient)
    prescriptions = Prescription.objects.filter(appointment__patient=patient)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="patient_{patient.id}_report.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # 🔷 Title
    p.setFont("Helvetica-Bold", 18)
    p.setFillColor(colors.darkblue)
    p.drawCentredString(width / 2, height - 2 * cm, "Patient Medical Report")

    # 🔷 Date
    p.setFont("Helvetica", 10)
    p.setFillColor(colors.black)
    p.drawRightString(width - 2 * cm, height - 2.8 * cm, f"Date: {date.today()}")

    # 🔷 Patient Info
    y = height - 4 * cm
    p.setFont("Helvetica-Bold", 12)
    p.drawString(2 * cm, y, "Patient Information")
    y -= 0.7 * cm

    p.setFont("Helvetica", 11)
    p.drawString(2 * cm, y, f"Name: {patient.first_name} {patient.last_name}")
    y -= 0.5 * cm
    # p.drawString(2 * cm, y, f"Age: {patient.age}")
    y -= 0.5 * cm
    p.drawString(2 * cm, y, f"Phone: {patient.phone}")

    # 🔷 Appointments
    y -= 1 * cm
    p.setFont("Helvetica-Bold", 12)
    p.drawString(2 * cm, y, "Appointments")
    y -= 0.6 * cm

    p.setFont("Helvetica", 10)
    for app in appointments:
        p.drawString(2 * cm, y, f"- {app.date} | Doctor: {app.doctor}")
        y -= 0.4 * cm
        if y < 3 * cm:
            p.showPage()
            y = height - 3 * cm

    # 🔷 Prescriptions
    y -= 0.6 * cm
    p.setFont("Helvetica-Bold", 12)
    p.drawString(2 * cm, y, "Prescriptions")
    y -= 0.6 * cm

    p.setFont("Helvetica", 10)
    for pre in prescriptions:   # isticmaal queryset‑ka
        medicines_list = pre.medicines.split(',')
        dosage_list = pre.dosage.split(',')

        if len(dosage_list) < len(medicines_list):
            dosage_list += ["N/A"] * (len(medicines_list) - len(dosage_list))

        for med, dose in zip(medicines_list, dosage_list):
            med = med.strip()
            dose = dose.strip()
            p.drawString(2 * cm, y, f"- {med} | Dose: {dose}")
            y -= 0.4 * cm
            if y < 3 * cm:
                p.showPage()
                y = height - 3 * cm

    # 🔷 Footer
    p.setFont("Helvetica-Oblique", 9)
    p.setFillColor(colors.grey)
    p.drawCentredString(width / 2, 1.5 * cm, "Generated by Patient Management System")

    p.showPage()
    p.save()
    return response



@login_required
def add_doctor_view(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Hal mar kaliya save
            return redirect('doctor_list')  # Redirect kadib save
    else:
        form = DoctorForm()
    return render(request, 'add_doctor.html', {'form': form})

def doctor_list_view(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctor_list.html', {'doctors': doctors})



# Delete doctor view
def delete_doctor_view(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        doctor.delete()
        return redirect('doctor_list')
    return render(request, 'delete_doctor.html', {'doctor': doctor})





class RecordListView(ListView):
    model = MedicalRecord
    template_name = 'record_list.html'
    context_object_name = 'records'

class RecordDetailView(DetailView):
    model = MedicalRecord
    template_name = 'record_detail.html'
    # KHADKAN HOOSE AYAA MUHIIM AH:
    context_object_name = 'record' 

class RecordCreateView(CreateView):
    model = MedicalRecord
    form_class = MedicalRecordForm
    template_name = 'record_form.html'
    success_url = reverse_lazy('record_list')


