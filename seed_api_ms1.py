import random
import time
import requests
from faker import Faker
import re

fake = Faker()

BASE_URL = "http://98.84.168.22:8000/api"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# 1. Crear propietarios
print("Creando propietarios...")
prop_ids = []

for i in range(5000):
    data = {
        "nombre": fake.name(),
        "correo": fake.unique.email(),
        "telefono": re.sub(r'\D', '', fake.phone_number())[:20]
    }
    try:
        response = requests.post(f"{BASE_URL}/propietarios/", json=data, headers=HEADERS, timeout=5)
        if response.status_code == 201:
            prop_ids.append(response.json().get('id'))
        else:
            print(f"[{i}] ❌ Error creando propietario:", response.status_code)
    except Exception as e:
        print(f"[{i}] ⚠️ Excepción creando propietario:", e)
    
    if i % 1 == 0:
        print(f"→ {i} propietarios procesados...")
    time.sleep(0.01)

print(f"✅ Total propietarios creados: {len(prop_ids)}")

# Validación
if not prop_ids:
    print("❌ No se crearon propietarios. Abortando creación de mascotas.")
    exit()

# 2. Crear mascotas
print("Creando mascotas...")
for i in range(20000):
    data = {
        "nombre": fake.first_name(),
        "especie": random.choice(["Perro", "Gato", "Conejo", "Loro", "Iguana"]),
        "raza": fake.word(),
        "edad": random.randint(1, 20),
        "propietario": random.choice(prop_ids)
    }
    try:
        response = requests.post(f"{BASE_URL}/mascotas/", json=data, headers=HEADERS, timeout=5)
        if response.status_code != 201:
            print(f"🐾 Error mascota {i}: {response.status_code}")
    except Exception as e:
        print(f"🐾 Excepción creando mascota {i}:", e)
    
    if i % 500 == 0:
        print(f"→ {i} mascotas procesadas...")
        time.sleep(0.5)

print("🎉 Inserción completa: 20000 mascotas registradas.")
