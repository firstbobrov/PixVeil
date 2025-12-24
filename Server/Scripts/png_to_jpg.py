from PIL import Image
import os

def png_to_jpg(png_path):
    """
    Преобразует PNG изображение в JPG и сохраняет в папку Temp
    
    Args:
        png_path (str): Путь к исходному PNG файлу
    
    Returns:
        str: Путь к сохраненному JPG файлу или None в случае ошибки
    """
    try:
        # Проверяем, существует ли исходный файл
        if not os.path.exists(png_path):
            print(f"Ошибка: файл '{png_path}' не найден")
            return None
        
        # Проверяем расширение файла
        if not png_path.lower().endswith('.png'):
            print(f"Предупреждение: файл '{png_path}' не имеет расширения .png")
        
        # Создаем папку Temp, если она не существует
        temp_dir = "../Temp"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
            print(f"Создана папка: {temp_dir}")
        
        # Открываем изображение
        with Image.open(png_path) as img:
            # Конвертируем RGBA в RGB, если есть альфа-канал (прозрачность)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Создаем белый фон для прозрачных областей
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Формируем путь для сохранения
            filename = os.path.splitext(os.path.basename(png_path))[0]
            jpg_path = os.path.join(temp_dir, f"{filename}.jpg")
            
            # Сохраняем как JPG с хорошим качеством
            img.save(jpg_path, 'JPEG', quality=95)
            
            print(f"Изображение сохранено: {jpg_path}")
            return jpg_path
            
    except Exception as e:
        print(f"Ошибка при конвертации: {e}")
        return None


# Пример использования
if __name__ == "__main__":
    
    result = png_to_jpg("../../Prefab_images/test.png")
    
    if result:
        print(f"Конвертация успешно завершена: {result}")
    else:
        print("Конвертация не удалась")
