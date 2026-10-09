import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main_parking_system_proj.settings')
django.setup()

from core_parking_system_app1.models import Defect

# Common parking system defects and their frequencies
defects = [
    ('Barrier Malfunction', 45),
    ('Ticket Printer Jam', 30),
    ('Payment Gateway Failure', 15),
    ('Sensor Error', 7),
    ('Software Crash', 3)
]

for d_type, freq in defects:
    Defect.objects.get_or_create(defect_type=d_type, defaults={'frequency': freq})

print("Defect data seeded successfully!")
