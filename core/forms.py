from django import forms
from django.forms import ModelForm

from core.models import Appointment, Patient, Prescription
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm
from django.contrib.auth.models import User
from .models import Medicine , Doctor , MedicalRecord
# from .forms import MedicineForm  



class DoctorForm(forms.ModelForm):
    SPECIALIZATION_CHOICES = [
        ('Cardiologist', 'Cardiologist'),
        ('Dermatologist', 'Dermatologist'),
        ('Neurologist', 'Neurologist'),
        ('Pediatrician', 'Pediatrician'),
        ('Dentist', 'Dentist'),
        ('General', 'General'),
    ]

    specialization = forms.ChoiceField(choices=SPECIALIZATION_CHOICES, widget=forms.Select(attrs={'class': 'border p-2 rounded w-full'}))

    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'specialization', 'profile_image']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'border p-2 rounded w-full'}),
            'last_name': forms.TextInput(attrs={'class': 'border p-2 rounded w-full'}),
        }
class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'quantity', 'price', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'border rounded px-3 py-2 w-full',
                'placeholder': 'Magaca dawo'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'border rounded px-3 py-2 w-full',
                'placeholder': 'Tirada'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'border rounded px-3 py-2 w-full',
                'placeholder': 'Qiimaha'
            }),
            'description': forms.Textarea(attrs={
                'class': 'border rounded px-3 py-2 w-full',
                'placeholder': 'Sharaxaad',
                'rows': 3
            }),
        }



class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full rounded-lg border-gray-300 focus:border-teal-500 focus:ring-teal-500'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full rounded-lg border-gray-300 focus:border-teal-500 focus:ring-teal-500'
    }))



class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full mb-3 rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500'
            })



# ---------------- FORMS ----------------
# class PatientForm(ModelForm):
    # class Meta:
        # model = Patient
        # fields = '__all__'


class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'


class PrescriptionForm(forms.ModelForm):
    medicine = forms.ModelChoiceField(
        queryset=Medicine.objects.all(),
        required=True,
        widget=forms.Select(attrs={
            'class': 'border rounded px-3 py-2 w-full',
            'placeholder': 'Dooro dawo'
        }),
        label='Dawo',
        empty_label='Dooro dawo...'
    )
    
    class Meta:
        model = Prescription
        fields = [
            'medicine',
            'diagnosis',
            'dosage',
            'quantity'
        ]
        widgets = {
            'diagnosis': forms.Textarea(attrs={
                'class': 'border rounded px-3 py-2 w-full',
                'rows': 3,
                'placeholder': 'Qor diagnosis'
            }),
            'dosage': forms.TextInput(attrs={
                'class': 'border rounded px-3 py-2 w-full',
                'placeholder': 'Qor dosage'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'border rounded px-3 py-2 w-full',
                'placeholder': 'Tirada'
            }),
        }


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
        }

class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'patient', 'date', 'time', 'status']





class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = '__all__'
        widgets = {
            'symptoms': forms.Textarea(attrs={'rows': 3, 'class': 'form-input'}),
            'diagnosis': forms.Textarea(attrs={'rows': 3, 'class': 'form-input'}),
            'treatment_plan': forms.Textarea(attrs={'rows': 3, 'class': 'form-input'}),
        } 
