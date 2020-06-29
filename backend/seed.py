import django
import os
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'phoenixware_backend.settings')
django.setup()
from django_seed import Seed
from apps.riesgo.models import Riesgo

seeder = Seed.seeder()
seeder.add_entity(Riesgo, 10, {
    'codigo': lambda x: random.randint(0, 1000)
})
inserted_pks = seeder.execute()
