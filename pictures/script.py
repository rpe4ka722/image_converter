from PIL import ImageFilter
import os
from PIL import Image


directory = r'C:\Users\rpe4ka722\Desktop\Android  project\kivy_venv\pictures'
for filename in os.listdir(directory):
    img = Image.open(os.path.join(directory, filename))
    print(img.format)
    print(img.mode)

    img.resize((99,99)).save(os.path.join(directory, 'small_' + filename))
