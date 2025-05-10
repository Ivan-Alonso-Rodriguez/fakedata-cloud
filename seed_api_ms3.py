import requests
import random
from faker import Faker

fake = Faker()

# MS2: Obtener consultas reales
MS2_URL = "http://lb-proyecto-1773710960.us-east-1.elb.amazonaws.com:3000"
# MS3: Subida de imágenes
MS3_URL = "http://lb-proyecto-1773710960.us-east-1.elb.amazonaws.com:5000"

print("📡 Obteniendo consultas desde MS2...")
try:
    res = requests.get(f"{MS2_URL}/consultas")
    if res.status_code == 200:
        consulta_ids = [c['id'] for c in res.json()]
        print(f" {len(consulta_ids)} consultas obtenidas")
    else:
        raise Exception("Respuesta no válida:", res.status_code)
except Exception as e:
    print("No se pudo obtener consultas:", e)
    exit(1)

print("Subiendo imágenes a MS3...")
for i in range(100):  # número de imágenes a insertar
    try:
        consulta_id = random.choice(consulta_ids)

        with open("imagen_fake.png", "rb") as f:
            files = {
                "file": ("imagen_fake.png", f, "image/png")
            }
            data = {
                "consultaId": consulta_id
            }

            response = requests.post(f"{MS3_URL}/Images/upload", files=files, data=data)
            if response.status_code in [200, 201]:
                res_json = response.json()
                print(f"Imagen {i+1} subida con consultaId {consulta_id}, ID imagen: {res_json.get('id')}")
            else:
                print(f"[{i}] Error:", response.status_code, response.text)
    except Exception as e:
        print(f"[{i}] Excepción:", e)

print("Proceso de carga de imágenes finalizado")
