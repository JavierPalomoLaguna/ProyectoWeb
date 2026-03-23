from PIL import Image
import os

img_dir = r"ProyectoWebApp\static\ProyectoWebApp\img"

for filename in os.listdir(img_dir):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        ruta = os.path.join(img_dir, filename)
        nombre_webp = os.path.splitext(filename)[0] + ".webp"
        ruta_webp = os.path.join(img_dir, nombre_webp)
        img = Image.open(ruta)
        img.save(ruta_webp, "webp", quality=85)
        print(f"Convertida: {nombre_webp}")