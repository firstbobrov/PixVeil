from PIL import Image
import os

def jpg_to_png(jpg_path):
    """
    Преобразует JPG изображение в PNG и сохраняет в папку Temp
    
    Args:
        jpg_path (str): Путь к исходному JPG файлу
    
    Returns:
        str: Путь к сохраненному PNG файлу или None в случае ошибки
    """
    try:
        # Проверяем, существует ли исходный файл
        if not os.path.exists(jpg_path):
            print(f"Ошибка: файл '{jpg_path}' не найден")
            return None
        
        # Проверяем расширение файла
        if not jpg_path.lower().endswith(('.jpg', '.jpeg')):
            print(f"Предупреждение: файл '{jpg_path}' не имеет расширения .jpg/.jpeg")
        
        # Создаем папку Temp, если она не существует
        temp_dir = "../Temp"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
            print(f"Создана папка: {temp_dir}")
        
        # Открываем изображение
        with Image.open(jpg_path) as img:
            # Конвертируем в RGB, если необходимо
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Формируем путь для сохранения
            filename = os.path.splitext(os.path.basename(jpg_path))[0]
            png_path = os.path.join(temp_dir, f"{filename}.png")
            
            # Сохраняем как PNG
            img.save(png_path, 'PNG')
            
            print(f"Изображение сохранено: {png_path}")
            return png_path
            
    except Exception as e:
        print(f"Ошибка при конвертации: {e}")
        return None


# Пример использования
if __name__ == "__main__":

    result = jpg_to_png("../../Prefab_images/test.jpg")
    
    if result:
        print(f"Конвертация успешно завершена: {result}")
    else:
        print("Конвертация не удалась")
