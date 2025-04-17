from PIL import Image, ImageDraw, ImageFont
import random
import os

def generate_plate_numbers(n=100):
    provinces = list("ABDEFGHJKLMNPRSTVWXYZ")
    letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    
    plate_numbers = set()
    while len(plate_numbers) < n:
        prefix = random.choice(provinces)
        number = str(random.randint(1000, 9999))
        suffix = "".join(random.choices(letters, k=random.choice([2, 3])))
        plate = f"{prefix}{number}{suffix}"
        plate_numbers.add(plate)
    
    return sorted(plate_numbers)

generated_plates = generate_plate_numbers(100)

output_dir = "F:/Codes/Dataset/tesseract"
os.makedirs(output_dir, exist_ok=True)

font_path = "F:/Codes/Dataset/tesseract/plat_nomor/PlatNomor.ttf"  
font_size = 100

for idx, text in enumerate(generated_plates):
    image = Image.new('L', (800, 150), 255)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)
    draw.text((10, 10), text, font=font, fill=0)

    filename_base = f"train-{idx}-{text}"
    tif_path = os.path.join(output_dir, f"{filename_base}.tif")
    image.save(tif_path, format='TIFF')

print(f"✅ Berhasil generate {len(generated_plates)} file .tif ke folder '{output_dir}'")
