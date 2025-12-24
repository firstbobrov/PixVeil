import numpy as np
from PIL import Image
import os

def save_image_from_rgb(rgb_matrix, filename, save_as_jpg=True):
    """
    Сохраняет RGB матрицу как изображение
    
    Args:
        rgb_matrix: numpy array с формой (H, W, 3)
        filename: имя исходного файла (например 'test.jpg')
        save_as_jpg: если True - сохраняет как JPG, если False - как PNG
    """
    # Создаем папку Temp если ее нет
    output_dir = "../Temp"
    os.makedirs(output_dir, exist_ok=True)
    
    # Разделяем имя файла и расширение
    name, ext = os.path.splitext(filename)
    
    # Формируем новое имя файла
    if save_as_jpg:
        output_filename = f"{name}_output.jpg"
    else:
        output_filename = f"{name}_output.png"
    
    output_path = os.path.join(output_dir, output_filename)
    
    # Конвертируем numpy array в изображение и сохраняем
    img = Image.fromarray(rgb_matrix.astype('uint8'))
    img.save(output_path)
    print("Изображение сохранено")
    
    return output_path

#пример

#!!!
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
#!!!
    
save_image_from_rgb(load_image_to_rgb("test.jpg"), "test", False)
