import numpy as np
from PIL import Image
import cv2
import random

# -------------------- Базовый алгоритм --------------------
def base_max_message_length(image_path):
    """Возвращает максимальное количество символов для базового алгоритма."""
    img = Image.open(image_path).convert('RGB')
    pixel_matrix = np.array(img)
    height, width, _ = pixel_matrix.shape
    return height * width - 1  # минус пиксель для длины


def base_encrypt(input_path, output_path, message):
    """Шифрование базовым алгоритмом. Возвращает (success, written)."""
    message_bytes = message.encode('utf-8')
    message_array = np.frombuffer(message_bytes, dtype=np.uint8)
    msg_len = len(message_array)

    img = Image.open(input_path).convert('RGB')
    pixel_matrix = np.array(img)
    height, width, _ = pixel_matrix.shape

    msg_index = 0
    flag = True

    for y in range(height):
        for x in range(width):
            if msg_index >= msg_len:
                break
            target = message_array[msg_index]
            current_red = pixel_matrix[y, x, 0]

            if flag:
                if abs(int(current_red) - msg_len) <= 10:
                    pixel_matrix[y, x, 0] = msg_len * 2
                    if pixel_matrix[y, x, 1] % 2 == 1:
                        pixel_matrix[y, x, 1] -= 1
                    if pixel_matrix[y, x, 2] % 2 == 1:
                        pixel_matrix[y, x, 2] -= 1
                    flag = False
                    continue

            if abs(int(current_red) - int(target)) <= 10:
                pixel_matrix[y, x, 0] = target
                if pixel_matrix[y, x, 1] % 2 == 1:
                    pixel_matrix[y, x, 1] -= 1
                if pixel_matrix[y, x, 2] % 2 == 1:
                    pixel_matrix[y, x, 2] -= 1
                msg_index += 1
            else:
                if pixel_matrix[y, x, 1] % 2 == 0:
                    pixel_matrix[y, x, 1] += 1
                if pixel_matrix[y, x, 2] % 2 == 0:
                    pixel_matrix[y, x, 2] += 1

        if msg_index >= msg_len:
            break

    output_img = Image.fromarray(pixel_matrix)
    output_img.save(output_path, 'PNG')
    success = (msg_index == msg_len)
    return success, msg_index


def base_decrypt(input_path):
    """Дешифрование базовым алгоритмом."""
    img = Image.open(input_path).convert('RGB')
    pixel_matrix = np.array(img)
    height, width, _ = pixel_matrix.shape

    extracted_bytes = []
    flag = True
    c = height * width

    for y in range(height):
        for x in range(width):
            if len(extracted_bytes) == c:
                break
            if pixel_matrix[y, x, 1] % 2 == 0:
                if flag:
                    c = int(pixel_matrix[y, x, 0] / 2)
                    flag = False
                    continue
                red = pixel_matrix[y, x, 0]
                extracted_bytes.append(red)
        if len(extracted_bytes) == c:
            break

    message_bytes = bytes(extracted_bytes[:c])
    return message_bytes.decode('utf-8', errors='ignore')


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

THRESHOLD = 10  # порог для поиска подходящих пикселей


def modified_max_message_length(image_path):
    """Возвращает оценку максимального количества символов (завышена, но используется для предупреждения)."""
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if image is None:
        return 0
    height, width = image.shape[:2]
    return height * width  # максимально возможное (все пиксели)


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


def _process_pixel(image_bgra, height, width, message, size_img, cnt_znach_pix):
    color_pixel = image_bgra[height, width].copy()
    if len(message) <= 0:
        _neznach_pixel(color_pixel, image_bgra, height, width, size_img)
        return cnt_znach_pix, message

    # Используем глобальный порог THRESHOLD
    mass = [abs(i - message[0]) <= THRESHOLD for i in image_bgra[height, width][0:-1]]
    if True in mass:
        cnt_znach_pix += 1
        red_flag = False
        if size_img:
            for index, color_code in enumerate(mass):
                if color_code and not red_flag:
                    red_flag = True
                    color_pixel[index] = message[0]
                    color_pixel[-1] = _create_alpha_pixel(index, color_pixel[-1])
                else:
                    color_pixel[index] = _create_chet(color_pixel[index])
        else:
            for index, color_code in enumerate(mass):
                if color_code and not red_flag:
                    red_flag = True
                    color_pixel[index] = message[0]
                    color_pixel[-1] = _create_alpha_pixel(index, color_pixel[-1])
                else:
                    color_pixel[index] = _create_ne_chet(color_pixel[index])
        image_bgra[height, width] = color_pixel
        message = message[1:]
    else:
        _neznach_pixel(color_pixel, image_bgra, height, width, size_img)
    return cnt_znach_pix, message


def modified_encrypt(input_path, output_path, message):
    """Шифрование модифицированным алгоритмом. Возвращает (success, written)."""
    message_indices = [SYMBOLS.index(ch) for ch in message if ch in SYMBOLS]
    if not message_indices:
        return False, 0

    image = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if image is None:
        raise ValueError("Не удалось загрузить изображение")
    if image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    size = image.shape

    size_img = (size[0] * size[1]) % 2 == 0
    cnt_znach_pix = 0
    image_bgra = image.copy()

    for height in range(size[0]):
        for width in range(size[1]):
            cnt_znach_pix, message_indices = _process_pixel(
                image_bgra, height, width, message_indices, size_img, cnt_znach_pix
            )

    cv2.imwrite(output_path, image_bgra)
    success = (cnt_znach_pix == len(message_indices))  # message_indices уже укорочен
    return success, cnt_znach_pix


def _chet_mas(a):
    return sum(1 for i in a if i % 2 == 0) >= 2


def _ne_chet_mas(a):
    return sum(1 for i in a if i % 2 != 0) >= 2


def modified_decrypt(input_path):
    image = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if image is None:
        raise ValueError("Не удалось загрузить изображение")
    size = image.shape

    size_img = (size[0] * size[1]) % 2 == 0
    message = ''
    for height in range(size[0]):
        for width in range(size[1]):
            mas_pix = image[height, width]
            if size_img:
                if _chet_mas(mas_pix[0:-1]):
                    idx = mas_pix[mas_pix[-1] % 3]
                    message += SYMBOLS[idx]
            else:
                if _ne_chet_mas(mas_pix[0:-1]):
                    idx = mas_pix[mas_pix[-1] % 3]
                    message += SYMBOLS[idx]
    return message