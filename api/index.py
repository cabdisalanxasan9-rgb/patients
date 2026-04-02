import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "patient.settings")

from patient.wsgi import application

app = application
