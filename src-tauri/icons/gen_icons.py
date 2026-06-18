from PIL import Image
import os

ico_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
img = Image.open(ico_path)

# Generate different sizes
sizes = {
    '32x32.png': 32,
    '128x128.png': 128,
    '128x128@2x.png': 256,
    'icon.png': 256,
}

for filename, size in sizes.items():
    resized = img.resize((size, size), Image.LANCZOS)
    output_path = os.path.join(os.path.dirname(__file__), filename)
    resized.save(output_path)
    print(f'Created {filename} ({size}x{size})')

# Copy as icns placeholder
import shutil
icns_path = os.path.join(os.path.dirname(__file__), 'icon.icns')
shutil.copy(os.path.join(os.path.dirname(__file__), 'icon.png'), icns_path)
print('Created icon.icns (placeholder)')
