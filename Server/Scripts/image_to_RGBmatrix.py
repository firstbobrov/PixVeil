import numpy as np
from PIL import Image
import os

def load_image_to_rgb(filename):
    base_path = "../../Prefab_images"
    filepath = os.path.join(base_path, filename)
    
    try:
        img = Image.open(filepath)
        img_rgb = img.convert('RGB')
        return np.array(img_rgb)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {filename} не найден в {base_path}")
    except Exception as e:
        raise Exception(f"Ошибка при загрузке изображения: {e}")

#пример

print(load_image_to_rgb("test.jpg"))
