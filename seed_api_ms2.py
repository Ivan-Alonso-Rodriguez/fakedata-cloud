import random
import requests
from faker import Faker

fake = Faker()

# Microservicio 2 (Consultas y Tratamientos)
BASE_URL = "http://lb-proyecto-1773710960.us-east-1.elb.amazonaws.com:3000"

# Microservicio 1 (Mascotas)
MS1_URL = "http://lb-proyecto-1773710960.us-east-1.elb.amazonaws.com:8000/api"

# 0. Obtener mascotaIds reales desde MS1
print("Obteniendo mascotaIds desde MS1...")
try:
    response = requests.get(f"{MS1_URL}/mascotas")
    if response.status_code == 200:
        mascota_ids = [m['id'] for m in response.json()]
        print(f"{len(mascota_ids)} mascotas obtenidas")
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")
except Exception as e:
    print("No se pudo obtener mascotas:", e)
    mascota_ids = list(range(1, 2000))  # fallback si falla

# 1. Crear 4,000 tratamientos vía API
print("Insertando tratamientos vía API...")
tratamiento_ids = []
for i in range(2000):
    data = {
        "nombre": fake.word().capitalize(),
        "descripcion": fake.sentence(nb_words=6)
    }
    try:
        response = requests.post(f"{BASE_URL}/tratamientos", json=data)
        if response.status_code == 201:
            tratamiento_ids.append(response.json()['id'])
        else:
            print(f"[{i}] Error creando tratamiento:", response.text)
    except Exception as e:
        print(f"[{i}] Excepción:", e)

    if (i + 1) % 100 == 0:
        print(f" {i + 1} tratamientos insertados...")

print(f" Total: {len(tratamiento_ids)} tratamientos insertados")

# 2. Crear 5,000 consultas vía API
print("Insertando consultas vía API...")
for i in range(2000):
    data = {
        "fecha": fake.date_time_between(start_date='-2y', end_date='now').isoformat(),
        "motivo": fake.sentence(nb_words=8),
        "mascotaId": random.choice(mascota_ids),
        "tratamientoIds": random.sample(tratamiento_ids, random.randint(1, 3))
    }
    try:
        response = requests.post(f"{BASE_URL}/consultas", json=data)
        if response.status_code != 201:
            print(f"[{i}]  Error creando consulta:", response.status_code, response.text)
    except Exception as e:
        print(f"[{i}]  Excepción creando consulta:", e)

    if (i + 1) % 100 == 0:
        print(f" {i + 1} consultas insertadas...")

print(" Fake data insertado vía API en MS2")
