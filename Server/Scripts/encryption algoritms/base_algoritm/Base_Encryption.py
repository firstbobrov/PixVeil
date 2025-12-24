from PIL import Image
import numpy as np

# Шаг 1: Входное сообщение
message = input('сообщение: ')  # Замените на реальное сообщение

# Шаг 2: Преобразование сообщения в массив чисел (байтов 0-255)
# Используем UTF-8 для поддержки русского, английского и других символов
message_bytes = message.encode('utf-8')
message_array = np.frombuffer(message_bytes, dtype=np.uint8)

# Шаг 3: Загрузка изображения с помощью Pillow и преобразование в NumPy массив
image_path = "Image.png"
img = Image.open(image_path)
pixel_matrix = np.array(img)  # Форма: (height, width, 3) для RGB

# Шаг 4: Проход по пикселям и запись в красный канал только если подходит (±10)
# Для подходящих: записать в red, сделать green и blue чётными
# Для неподходящих: сделать green и blue нечётными (используем | 1)
height, width, _ = pixel_matrix.shape
msg_index = 0
flag = True

for y in range(height):
    for x in range(width):
        if msg_index >= len(message_array):
            break  # Сообщение полностью записано, оставшиеся пиксели не трогаем
        
        target = message_array[msg_index]
        current_red = pixel_matrix[y, x, 0]
        
#!!!
        if flag:
            if abs(int(current_red) - len(message_array)) <= 10:
                # Подходит: записываем в red, делаем g и b чётными
                pixel_matrix[y, x, 0] = int(len(message_array))
                if pixel_matrix[y, x, 1] % 2 == 1:
                    pixel_matrix[y, x, 1] -= 1# Green to even
                if pixel_matrix[y, x, 2] % 2 == 1:
                    pixel_matrix[y, x, 2] -= 1# Blue to even
                print(int(len(message_array)/2))
                flag = False
                continue
#!!!
                
        if abs(int(current_red) - int(target)) <= 10:
            # Подходит: записываем в red, делаем g и b чётными
            pixel_matrix[y, x, 0] = target
            if pixel_matrix[y, x, 1] % 2 == 1:
                pixel_matrix[y, x, 1] -= 1# Green to even
            if pixel_matrix[y, x, 2] % 2 == 1:
                pixel_matrix[y, x, 2] -= 1# Blue to even
            msg_index += 1
        else:
            if pixel_matrix[y, x, 1] % 2 == 0:
                pixel_matrix[y, x, 1] += 1# Green to even
            if pixel_matrix[y, x, 2] % 2 == 0:
                pixel_matrix[y, x, 2] += 1# Blue to even
    
    if msg_index >= len(message_array):
        break

# Шаг 5: Экспорт измененной матрицы в новое изображение
output_img = Image.fromarray(pixel_matrix)
output_path = "image_output.png"
output_img.save(output_path)

print(f"Сообщение зашифровано в {output_path}")
