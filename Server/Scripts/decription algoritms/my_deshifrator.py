import time

import cv2

s = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
 'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л',
 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш',
 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я',
 'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л',
 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш',
 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я',
 ' ', '\t', '\n', '\r',  # пробел, табуляция, перенос строки
 '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-',
 '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^',
 '_', '`', '{', '|', '}', '~'] + [' ']*100


# Читаем изображение со всеми каналами (включая альфа-канал)
image = cv2.imread('kapitan_vk.png', cv2.IMREAD_UNCHANGED)

size = image.shape
print(f"Исходный размер: {size}")
print(f"Тип данных: {image.dtype}")


size_img = (size[0] * size[1]) % 2 == 0  # True если четное количество пикселей
print(f'Размер изображения четное число: {size_img}')


def chet_mas(a: list):
    a = [True if i%2==0 else False for i in a].count(True)
    if a >= 2:
        return True
    return False


def ne_chet_mas(a: list):
    a = [True if i%2!=0 else False for i in a].count(True)
    if a >= 2:
        return True
    return False

stat_t = time.time()
message = ''
if size_img:
    for height in range(size[0]):
        for width in range(size[1]):
            mas_pix = image[height, width]
            if chet_mas(mas_pix[0:-1]):
                # print(mas_pix)
                x = mas_pix[mas_pix[-1] % 3]
                # print(x)
                # print(s[x])
                # print()
                message += s[x]
else:
    for height in range(size[0]):
        for width in range(size[1]):
            mas_pix = image[height, width]
            if ne_chet_mas(mas_pix[0:-1]):
                x = mas_pix[mas_pix[-1] % 3]
                message += s[x]

print(f'Время расшифровки: {time.time() - stat_t} сек.')
print(f'Длина расшифрованного сообщения: {len(message)}')
print(message)

with open('my_deshifr_message.txt', 'w', encoding='utf-8') as f:
    f.write(message)
