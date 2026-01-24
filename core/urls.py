from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
path('' , views.login_view, name='login'), 
path('signup/', views.signup_view, name='signup'),

path('dashbord/', views.dashbord, name='dashbord'),

path('patient_list', views.patient_list, name='patient_list'),


path('patients/add/', views.patient_create, name='patient_create'),
path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),


path('appointments/', views.appointment_list, name='appointment_list'),
path('appointments/add/', views.appointment_create, name='appointment_create'),
path('appointments/add/', views.appointment_create, name='appointment_create'),


path('prescription/add/<int:appointment_id>/', views.prescription_create, name='prescription_create'),



path('patients/edit/<int:pk>/', views.patient_update, name='patient_update'),
path('patients/delete/<int:pk>/', views.patient_delete, name='patient_delete'),
path('patients/delete/<int:pk>/', views.patient_delete, name='patient_delete'),


path('prescription/<int:appointment_id>/', views.create_prescription, name='create_prescription'),

path('prescriptions/', views.prescription_list, name='prescription_list'),


path('signup/', views.signup_view, name='signup'),
path('login/' , views.login_view, name='login'),
path('logout/', views.logout_view, name='logout'),


path('medicines/', views.medicine_list, name='medicine_list'),
path('medicines/add/', views.medicine_add, name='medicine_add'),
path('medicines/<int:pk>/', views.medicine_detail, name='medicine_detail'),
path('medicines/<int:pk>/edit/', views.medicine_edit, name='medicine_edit'),
path('medicines/<int:pk>/delete/', views.medicine_delete, name='medicine_delete'),
path('patient/<int:pk>/report/', views.patient_report, name='patient_report'),
path('add-doctor/', views.add_doctor_view, name='add_doctor'),
path('doctors/', views.doctor_list_view, name='doctor_list'),
path('delete-doctor/<int:pk>/', views.delete_doctor_view, name='delete_doctor'),
path('RecordList', views.RecordListView.as_view(), name='record_list'),
path('add/', views.RecordCreateView.as_view(), name='record_create'),
path('<int:pk>/', views.RecordDetailView.as_view(), name='record_detail'),


]