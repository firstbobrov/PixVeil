import numpy as np
from PIL import Image
import cv2
import random


# -------------------- Базовый алгоритм (обновлённый) --------------------
def base_max_message_length(image_path):
    """Возвращает максимальное количество символов для базового алгоритма."""
    img = Image.open(image_path).convert('RGB')
    pixel_matrix = np.array(img)
    height, width, _ = pixel_matrix.shape
    return height * width - 1  # минус пиксель для длины (упрощённая оценка)


def base_encrypt(input_path, output_path, message):
    """
    Шифрование базовым алгоритмом (многобайтовая длина).
    Возвращает (success, written), где written – количество записанных байт сообщения.
    Выводит статистику, аналогичную Base_Encryption (1).py.
    """
    message_bytes = message.encode('utf-8')
    msg_len = len(message_bytes)

    # Формируем байты длины (каждый ≤255)
    len_bytes = []
    remaining = msg_len
    while remaining >= 255:
        len_bytes.append(255)
        remaining -= 255
    len_bytes.append(remaining)

    data_to_hide = len_bytes + list(message_bytes)

    img = Image.open(input_path).convert('RGB')
    pixel_matrix = np.array(img)
    height, width, _ = pixel_matrix.shape

    data_index = 0
    total_bytes = len(data_to_hide)
    encoded_message_bytes = 0  # сколько байт самого сообщения записано

    for y in range(height):
        for x in range(width):
            if data_index >= total_bytes:
                break
            target = data_to_hide[data_index]
            cur_red = int(pixel_matrix[y, x, 0])
            if abs(cur_red - target) <= 10:
                pixel_matrix[y, x, 0] = target
                if pixel_matrix[y, x, 1] % 2 == 1:
                    pixel_matrix[y, x, 1] -= 1
                if pixel_matrix[y, x, 2] % 2 == 1:
                    pixel_matrix[y, x, 2] -= 1
                # Считаем только байты самого сообщения (пропускаем длину)
                if data_index >= len(len_bytes):
                    encoded_message_bytes += 1
                data_index += 1
            else:
                if pixel_matrix[y, x, 1] % 2 == 0:
                    pixel_matrix[y, x, 1] += 1
                if pixel_matrix[y, x, 2] % 2 == 0:
                    pixel_matrix[y, x, 2] += 1
        if data_index >= total_bytes:
            break

    output_img = Image.fromarray(pixel_matrix)
    output_img.save(output_path, 'PNG')

    # ---- Статистика в символах (как в Base_Encryption) ----
    total_symbols = len(message)
    written_bytes = message_bytes[:encoded_message_bytes]
    written_symbols = written_bytes.decode('utf-8', errors='ignore')
    symbols_count = len(written_symbols)

    print(f"Изображение сохранено")
    print(f"Всего символов в сообщении: {total_symbols}")
    print(f"Зашифровано символов: {symbols_count}")
    if symbols_count < total_symbols:
        print(f"⚠️ Не хватило пикселей. Зашифровано только {symbols_count} из {total_symbols} символов.")
    else:
        print("✓ Сообщение зашифровано полностью.")

    success = (encoded_message_bytes == msg_len)
    return success, encoded_message_bytes


def base_decrypt(input_path):
    """
    Дешифрование базовым алгоритмом (многобайтовая длина).
    Возвращает расшифрованную строку.
    """
    img = Image.open(input_path).convert('RGB')
    pixel_matrix = np.array(img)
    height, width, _ = pixel_matrix.shape

    # Собираем все байты из красных каналов, где зелёный чётный
    extracted_all = []
    for y in range(height):
        for x in range(width):
            if pixel_matrix[y, x, 1] % 2 == 0:
                extracted_all.append(int(pixel_matrix[y, x, 0]))

    # Извлекаем байты длины (до первого <255)
    len_bytes = []
    idx = 0
    while idx < len(extracted_all):
        b = extracted_all[idx]
        len_bytes.append(b)
        idx += 1
        if b < 255:
            break

    total_len = sum(len_bytes)

    # Извлекаем байты сообщения
    if idx + total_len > len(extracted_all):
        # Недостаточно данных – возвращаем то, что есть
        message_bytes = extracted_all[idx:]
    else:
        message_bytes = extracted_all[idx:idx + total_len]

    return bytes(message_bytes).decode('utf-8', errors='ignore')


# -------------------- Модифицированный алгоритм (с порогом 10) --------------------
SYMBOLS = [
              '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
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
              ' ', '\t', '\n', '\r',
              '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-',
              '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^',
              '_', '`', '{', '|', '}', '~'
          ] + [' '] * 100

THRESHOLD = 10


def modified_max_message_length(image_path):
    """Возвращает оценку максимального количества символов (завышена)."""
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if image is None:
        return 0
    height, width = image.shape[:2]
    return height * width


def _create_chet(a: int) -> int:
    return a - 1 if a % 2 else a


def _create_ne_chet(a: int) -> int:
    return a + 1 if a % 2 == 0 else a


def _ost_del_3(a: int) -> int:
    return a % 3


def _minus_plus(a: int) -> bool:
    return a <= 253


def _create_alpha_pixel(znach_index, code_alpha_chanel):
    mod = _ost_del_3(code_alpha_chanel)
    if mod == 0:
        if znach_index == 0:
            pass
        elif znach_index == 1:
            code_alpha_chanel = code_alpha_chanel + 1 if _minus_plus(code_alpha_chanel) else code_alpha_chanel - 2
        elif znach_index == 2:
            code_alpha_chanel = code_alpha_chanel + 2 if _minus_plus(code_alpha_chanel) else code_alpha_chanel - 1
    elif mod == 1:
        if znach_index == 0:
            code_alpha_chanel = code_alpha_chanel + 2 if _minus_plus(code_alpha_chanel) else code_alpha_chanel - 1
        elif znach_index == 1:
            pass
        elif znach_index == 2:
            code_alpha_chanel = code_alpha_chanel + 1 if _minus_plus(code_alpha_chanel) else code_alpha_chanel - 2
    elif mod == 2:
        if znach_index == 0:
            code_alpha_chanel = code_alpha_chanel + 1 if _minus_plus(code_alpha_chanel) else code_alpha_chanel - 2
        elif znach_index == 1:
            code_alpha_chanel = code_alpha_chanel + 2 if _minus_plus(code_alpha_chanel) else code_alpha_chanel - 1
        elif znach_index == 2:
            pass
    return code_alpha_chanel


def _neznach_pixel(color_pix, image_bgra, height, width, size_img):
    new_mas = []
    if size_img:
        for color in color_pix[:-1]:
            new_mas.append(int(_create_ne_chet(color)))
        new_mas.append(int(_create_alpha_pixel(random.randint(0, 2), color_pix[-1])))
    else:
        for color in color_pix[:-1]:
            new_mas.append(int(_create_chet(color)))
        new_mas.append(int(_create_alpha_pixel(random.randint(0, 2), color_pix[-1])))
    image_bgra[height, width] = new_mas


def modified_encrypt(input_path, output_path, message):
    """
    Шифрование модифицированным алгоритмом с сохранением длины сообщения.
    Возвращает (success, written), где written – количество записанных символов.
    """
    total_symbols = len(message)
    # Отбираем только символы, присутствующие в SYMBOLS
    original_indices = [SYMBOLS.index(ch) for ch in message if ch in SYMBOLS]
    if not original_indices:
        print(f"Изображение сохранено")
        print(f"Всего символов в сообщении: {total_symbols}")
        print(f"Зашифровано символов: 0")
        print(f"⚠️ Не хватило пикселей. Зашифровано только 0 из {total_symbols} символов.")
        return False, 0

    image = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if image is None:
        raise ValueError("Не удалось загрузить изображение")
    if image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    size = image.shape

    # Кодируем длину сообщения (количество символов) в 4 байта (uint32)
    msg_len = len(original_indices)
    len_bytes = list(msg_len.to_bytes(4, byteorder='big'))

    # Объединяем байты длины и индексы символов
    data_to_hide = len_bytes + original_indices

    size_img = (size[0] * size[1]) % 2 == 0
    cnt_znach_pix = 0
    image_bgra = image.copy()
    data_index = 0
    total_data = len(data_to_hide)

    for height in range(size[0]):
        for width in range(size[1]):
            if data_index >= total_data:
                break
            color_pixel = image_bgra[height, width].copy()
            target = data_to_hide[data_index]

            # Проверяем, можно ли записать значение target в один из цветовых каналов (B,G,R)
            mass = [abs(int(i) - target) <= THRESHOLD for i in color_pixel[0:-1]]
            if True in mass:
                cnt_znach_pix += 1
                red_flag = False
                if size_img:
                    for idx, ok in enumerate(mass):
                        if ok and not red_flag:
                            red_flag = True
                            color_pixel[idx] = target
                            color_pixel[-1] = _create_alpha_pixel(idx, color_pixel[-1])
                        else:
                            color_pixel[idx] = _create_chet(color_pixel[idx])
                else:
                    for idx, ok in enumerate(mass):
                        if ok and not red_flag:
                            red_flag = True
                            color_pixel[idx] = target
                            color_pixel[-1] = _create_alpha_pixel(idx, color_pixel[-1])
                        else:
                            color_pixel[idx] = _create_ne_chet(color_pixel[idx])
                image_bgra[height, width] = color_pixel
                data_index += 1
            else:
                # Пиксель не подходит – делаем его незначащим
                _neznach_pixel(color_pixel, image_bgra, height, width, size_img)
        if data_index >= total_data:
            break

    cv2.imwrite(output_path, image_bgra)

    written_symbols = cnt_znach_pix - 4  # вычитаем 4 байта длины
    # Статистика
    print(f"Изображение сохранено")
    print(f"Всего символов в сообщении: {total_symbols}")
    print(f"Зашифровано символов: {written_symbols}")
    if written_symbols < total_symbols:
        print(f"⚠️ Не хватило пикселей. Зашифровано только {written_symbols} из {total_symbols} символов.")
    else:
        print("✓ Сообщение зашифровано полностью.")

    success = (data_index == total_data)
    return success, written_symbols


def _chet_mas(a):
    return sum(1 for i in a if i % 2 == 0) >= 2


def _ne_chet_mas(a):
    return sum(1 for i in a if i % 2 != 0) >= 2


def modified_decrypt(input_path):
    """
    Дешифрование модифицированным алгоритмом с чтением длины сообщения.
    Возвращает расшифрованную строку.
    """
    image = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if image is None:
        raise ValueError("Не удалось загрузить изображение")
    size = image.shape

    size_img = (size[0] * size[1]) % 2 == 0
    extracted = []  # список извлечённых значений (сначала длина, потом символы)

    for height in range(size[0]):
        for width in range(size[1]):
            mas_pix = image[height, width]
            if size_img:
                if _chet_mas(mas_pix[0:-1]):
                    idx = mas_pix[mas_pix[-1] % 3]
                    extracted.append(idx)
            else:
                if _ne_chet_mas(mas_pix[0:-1]):
                    idx = mas_pix[mas_pix[-1] % 3]
                    extracted.append(idx)

            # Как только извлекли 4 байта длины – определяем полную длину сообщения
            if len(extracted) == 4:
                msg_len = int.from_bytes(bytes(extracted[:4]), byteorder='big')
                # Если сообщение пустое, выходим
                if msg_len == 0:
                    break

        # Выходим, если извлекли всё сообщение
        if len(extracted) >= 4:
            msg_len = int.from_bytes(bytes(extracted[:4]), byteorder='big')
            if len(extracted) >= 4 + msg_len:
                break

    if len(extracted) < 4:
        return ""  # недостаточно данных

    msg_len = int.from_bytes(bytes(extracted[:4]), byteorder='big')
    # Извлекаем индексы символов
    indices = extracted[4:4 + msg_len]
    # Преобразуем индексы обратно в символы
    result = ''.join(SYMBOLS[i] for i in indices if i < len(SYMBOLS))
    return result