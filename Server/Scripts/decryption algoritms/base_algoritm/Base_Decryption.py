from PIL import Image
import numpy as np

# Шаг 1: Загрузка изображения с помощью Pillow и преобразование в NumPy массив
image_path = "image_output.png"  # Путь к зашифрованному изображению
img = Image.open(image_path)
pixel_matrix = np.array(img)  # Форма: (height, width, 3) для RGB

# Шаг 2: Проход по пикселям и извлечение байтов из red канала, если green чётный
height, width, _ = pixel_matrix.shape
extracted_bytes = []
flag = True
c = height * width
for y in range(height):
    for x in range(width):
#!!! доработать оптимизацию
        if len(extracted_bytes) == c:
            break
        if pixel_matrix[y, x, 1] % 2 == 0:
            if flag:
                c = int(int(pixel_matrix[y, x, 0])/2)
                print(c)
                flag = False
                continue
#!!!   
            # Чётный green - извлекаем red
            red = pixel_matrix[y, x, 0]
            extracted_bytes.append(red)

# Шаг 3: Преобразование списка байтов в bytes и декодирование как UTF-8
message_bytes = bytes(extracted_bytes)
decoded_message = message_bytes.decode('utf-8', errors='ignore')

print("Восстановленное сообщение:")
print(decoded_message)
