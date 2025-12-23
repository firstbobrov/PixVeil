import random
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
 '_', '`', '{', '|', '}', '~']


with open('message.txt', 'r', encoding='utf-8') as file:
    message = file.read()
print(f'Длина вышего сообщения: {len(message)}')
message = [s.index(char) for char in message if char in s]  # создаем список с номерами символов, если их нет в списке, то заменяем на код '~'
print(f'Длина выходного сообщения: {len(message)}')

# Читаем изображение со всеми каналами (включая альфа-канал)
image = cv2.imread('baterfly.png', cv2.IMREAD_UNCHANGED)

size = image.shape
print(f"Исходный размер: {size}")
print(f"Тип данных: {image.dtype}")

# Добавляем альфа-канал (в формате BGRA - правильный для OpenCV)
image_bgra = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)


def create_chet(a: int):
    if a%2 != 0:
        return a - 1
    return a

def create_ne_chet(a: int):
    if a%2 == 0:
        return a + 1
    return a

def ost_del_3(a: int):
    return a%3

def minus_plus(a: int):
    if a <= 253:
        return True  # +
    else:
        return False  # -

def create_alpha_pixel(znach_index, code_alpha_chanel):
    """создает нужное число в альфа-канале для
    определения в каком из каналов значимое число"""
    if ost_del_3(code_alpha_chanel) == 0:
        if znach_index == 0:
            code_alpha_chanel = code_alpha_chanel
        elif znach_index == 1:
            code_alpha_chanel = code_alpha_chanel + 1 if minus_plus(code_alpha_chanel) else code_alpha_chanel - 2
        elif znach_index == 2:
            code_alpha_chanel = code_alpha_chanel + 2 if minus_plus(code_alpha_chanel) else code_alpha_chanel - 1

    if ost_del_3(code_alpha_chanel) == 1:
        if znach_index == 0:
            code_alpha_chanel = code_alpha_chanel + 2 if minus_plus(code_alpha_chanel) else code_alpha_chanel - 1
        elif znach_index == 1:
            code_alpha_chanel = code_alpha_chanel
        elif znach_index == 2:
            code_alpha_chanel = code_alpha_chanel + 1 if minus_plus(code_alpha_chanel) else code_alpha_chanel - 2

    if ost_del_3(code_alpha_chanel) == 2:
        if znach_index == 0:
            code_alpha_chanel = code_alpha_chanel + 1 if minus_plus(code_alpha_chanel) else code_alpha_chanel - 2
        elif znach_index == 1:
            code_alpha_chanel = code_alpha_chanel + 2 if minus_plus(code_alpha_chanel) else code_alpha_chanel - 1
        elif znach_index == 2:
            code_alpha_chanel = code_alpha_chanel

    return code_alpha_chanel


size_img = (size[0] * size[1]) % 2 == 0  # True если четное количество пикселей

def neznach_pixel(color_pix):
    """Шифрование незначимых пикселей"""
    print(color_pix)
    new_mas = []
    if size_img:
        for color in color_pix[:-1]:
            new_mas.append(int(create_ne_chet(color)))
        new_mas.append(int(create_alpha_pixel(random.randint(0, 2), color_pix[-1])))
    else:
        for color in color_pix[:-1]:
            new_mas.append(int(create_chet(color)))
        new_mas.append(int(create_alpha_pixel(random.randint(0, 2), color_pix[-1])))
    image_bgra[height, width] = new_mas
    # print(f'\nИзмененный незначимый пиксель: {new_mass}\n')

start_t = time.time()
cnt_znach_pix = 0
for height in range(size[0]):
    for width in range(size[1]):
        # print(f'Исходный пиксель: {image_bgra[height, width]}')
        color_pixel = image_bgra[height, width].copy()
        # проверка на пустое сообщение
        if len(message) <= 0:
            neznach_pixel(color_pixel)
            continue
        mass = [abs(i - message[0]) <= 1 for i in image_bgra[height, width][0:-1]]
        if True in mass:
            cnt_znach_pix += 1
            red_flag = False
            # print(f'\nИсходный пиксель: {image_bgra[height, width]}')
            # print(f'Шифруем символ "{s[message[0]]}" под номером: {message[0]}')
            if size_img:
                for index, color_code in enumerate(mass):
                    if color_code and not red_flag:
                        red_flag = True
                        color_pixel[index] = message[0]
                        color_pixel[-1] = create_alpha_pixel(index, color_pixel[-1])
                    else:
                        color_pixel[index] = create_chet(color_pixel[index])
                        # print(f'создан четный пиксель: {color_pixel[index]}')
            else:
                for index, color_code in enumerate(mass):
                    if color_code and not red_flag:
                        red_flag = True
                        color_pixel[index] = message[0]
                        color_pixel[-1] = create_alpha_pixel(index, color_pixel[-1])
                    else:
                        color_pixel[index] = create_ne_chet(color_pixel[index])
                        # print(f'создан нечетный пиксель: {color_pixel[index]}')

            image_bgra[height, width] = color_pixel
            print(f'измененный пиксель: {color_pixel}\n')
            message = message[1:]  # удаляет из сообщения зашифрованный символ
            # print(cnt_znach_pix)

        else:
            neznach_pixel(color_pixel)
            # print(cnt_znach_pix)


print(f'Время затраченное на шифрование: {time.time() - start_t} cек.')
print(f'Всего зашифровано символов: {cnt_znach_pix}')
# Сохраняем в правильном формате (BGRA)
output_path = 'baterfly_bgra.png'
cv2.imwrite(output_path, image_bgra)
print(f"Изображение сохранено как: {output_path}")