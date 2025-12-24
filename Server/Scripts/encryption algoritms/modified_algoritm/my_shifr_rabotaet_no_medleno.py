import random
import time
import cv2

# Таблица символов для шифрования
# Содержит цифры, латинские буквы, кириллицу и специальные символы
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


def read_message():
    """
    Читает сообщение из файла и преобразует в список индексов символов.
    Если символ не найден в таблице s, он пропускается.
    """
    with open('message.txt', 'r', encoding='utf-8') as file:
        message = file.read()
    print(f'Длина вашего сообщения: {len(message)}')
    # Преобразуем символы в их индексы в таблице s
    message = [s.index(char) for char in message if char in s]
    print(f'Длина выходного сообщения: {len(message)}')
    return message


def load_image():
    """
    Загружает изображение и преобразует его в формат BGRA (с альфа-каналом).
    BGRA = Blue, Green, Red, Alpha
    """
    image = cv2.imread('kapitan.png', cv2.IMREAD_UNCHANGED)
    size = image.shape  # Размеры изображения (высота, ширина, каналы)
    print(f"Исходный размер: {size}")
    print(f"Тип данных: {image.dtype}")
    # Конвертируем в BGRA формат (добавляем альфа-канал)
    image_bgra = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    return image_bgra, size


def create_chet(a: int):
    """
    Делает число четным. Если число нечетное - уменьшает на 1.
    Пример: 5 → 4, 6 → 6
    """
    if a % 2 != 0:
        return a - 1
    return a


def create_ne_chet(a: int):
    """
    Делает число нечетным. Если число четное - увеличивает на 1.
    Пример: 4 → 5, 5 → 5
    """
    if a % 2 == 0:
        return a + 1
    return a


def ost_del_3(a: int):
    """Возвращает остаток от деления на 3 (0, 1 или 2)."""
    return a % 3


def minus_plus(a: int):
    """
    Определяет, можно ли увеличить число или нужно уменьшить.
    Возвращает True если можно увеличить (число ≤ 253),
    иначе False (нужно уменьшить).
    """
    if a <= 253:
        return True  # +
    else:
        return False  # -


def create_alpha_pixel(znach_index, code_alpha_chanel):
    """
    Модифицирует значение альфа-канала так, чтобы при декодировании
    можно было определить, в каком из RGB-каналов хранится информация.

    Принцип работы:
    - znach_index (0, 1, 2) показывает, в каком канале (B, G, R) спрятано значение
    - Изменяет альфа-канал так, чтобы code_alpha_chanel % 3 == znach_index
    """
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


def neznach_pixel(color_pix, image_bgra, height, width, size_img):
    """
    Обрабатывает 'незначимый' пиксель (не содержит данных сообщения).
    Модифицирует пиксель в соответствии с четностью изображения:
    - Если изображение четное: делает RGB-каналы нечетными
    - Если изображение нечетное: делает RGB-каналы четными
    Случайным образом выбирает, в каком канале 'хранить' мусорные данные.
    """
    new_mas = []
    if size_img:
        # Четное изображение: RGB-каналы делаем нечетными
        for color in color_pix[:-1]:
            new_mas.append(int(create_ne_chet(color)))
        # Случайно выбираем 'индекс' для альфа-канала
        new_mas.append(int(create_alpha_pixel(random.randint(0, 2), color_pix[-1])))
    else:
        # Нечетное изображение: RGB-каналы делаем четными
        for color in color_pix[:-1]:
            new_mas.append(int(create_chet(color)))
        new_mas.append(int(create_alpha_pixel(random.randint(0, 2), color_pix[-1])))
    image_bgra[height, width] = new_mas


def process_pixel(image_bgra, height, width, message, size_img, cnt_znach_pix):
    """
    Обрабатывает один пиксель изображения.
    Определяет, можно ли в этот пиксель записать символ из сообщения.
    """
    color_pixel = image_bgra[height, width].copy()

    # Если сообщение закончилось, обрабатываем как незначимый пиксель
    if len(message) <= 0:
        neznach_pixel(color_pixel, image_bgra, height, width, size_img)
        return cnt_znach_pix, message

    # Проверяем, отличается ли какой-либо из RGB-каналов
    # от текущего символа не более чем на 1
    mass = [abs(i - message[0]) <= 1 for i in image_bgra[height, width][0:-1]]

    if True in mass:
        # Нашли подходящий пиксель для записи символа
        cnt_znach_pix += 1
        red_flag = False  # Флаг, что уже записали символ

        if size_img:
            # Четное изображение: оставляем выбранный канал как есть,
            # остальные делаем четными
            for index, color_code in enumerate(mass):
                if color_code and not red_flag:
                    red_flag = True
                    color_pixel[index] = message[0]  # Записываем символ
                    color_pixel[-1] = create_alpha_pixel(index, color_pixel[-1])  # Настраиваем альфа-канал
                else:
                    color_pixel[index] = create_chet(color_pixel[index])  # Делаем четным
        else:
            # Нечетное изображение: оставляем выбранный канал как есть,
            # остальные делаем нечетными
            for index, color_code in enumerate(mass):
                if color_code and not red_flag:
                    red_flag = True
                    color_pixel[index] = message[0]
                    color_pixel[-1] = create_alpha_pixel(index, color_pixel[-1])
                else:
                    color_pixel[index] = create_ne_chet(color_pixel[index])

        image_bgra[height, width] = color_pixel
        print(f'измененный пиксель: {color_pixel}\n')
        message = message[1:]  # Удаляем обработанный символ

    else:
        # Пиксель не подходит для записи символа
        neznach_pixel(color_pixel, image_bgra, height, width, size_img)

    return cnt_znach_pix, message


def encrypt_image(image_bgra, size, message):
    """
    Основная функция шифрования.
    Проходит по всем пикселям изображения и встраивает в него сообщение.
    """
    # Определяем, четное ли общее количество пикселей
    size_img = (size[0] * size[1]) % 2 == 0
    start_t = time.time()
    cnt_znach_pix = 0  # Счетчик зашифрованных символов

    # Обрабатываем каждый пиксель изображения
    for height in range(size[0]):
        for width in range(size[1]):
            cnt_znach_pix, message = process_pixel(image_bgra, height, width, message, size_img, cnt_znach_pix)

    print(f'Время затраченное на шифрование: {time.time() - start_t} сек.')
    print(f'Всего зашифровано символов: {cnt_znach_pix}')
    return image_bgra


def save_image(image_bgra):
    """Сохраняет зашифрованное изображение в файл."""
    output_path = 'kapitan_bgra.png'
    cv2.imwrite(output_path, image_bgra)
    print(f"Изображение сохранено как: {output_path}")


def main():
    """Главная функция программы. Оркестрирует весь процесс шифрования."""
    message = read_message()
    image_bgra, size = load_image()
    image_bgra = encrypt_image(image_bgra, size, message)
    save_image(image_bgra)


if __name__ == "__main__":
    main()