import time
import cv2

# Таблица символов для декодирования
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
     '_', '`', '{', '|', '}', '~'] + [' '] * 100


def load_image():
    """Загружает изображение со всеми каналами (включая альфа-канал)"""
    image = cv2.imread('kapitan_bgra.png', cv2.IMREAD_UNCHANGED)
    size = image.shape
    print(f"Исходный размер: {size}")
    print(f"Тип данных: {image.dtype}")
    return image, size


def chet_mas(a: list):
    """Проверяет, есть ли 2 или более четных значений в списке"""
    a = [True if i % 2 == 0 else False for i in a].count(True)
    return a >= 2


def ne_chet_mas(a: list):
    """Проверяет, есть ли 2 или более нечетных значений в списке"""
    a = [True if i % 2 != 0 else False for i in a].count(True)
    return a >= 2


def decode_message(image, size):
    """Декодирует сообщение из изображения"""
    size_img = (size[0] * size[1]) % 2 == 0  # True если четное количество пикселей
    print(f'Размер изображения четное число: {size_img}')

    message = ''

    if size_img:
        # Для четных изображений ищем пиксели с большинством четных RGB-значений
        for height in range(size[0]):
            for width in range(size[1]):
                mas_pix = image[height, width]
                if chet_mas(mas_pix[0:-1]):
                    x = mas_pix[mas_pix[-1] % 3]
                    message += s[x]
    else:
        # Для нечетных изображений ищем пиксели с большинством нечетных RGB-значений
        for height in range(size[0]):
            for width in range(size[1]):
                mas_pix = image[height, width]
                if ne_chet_mas(mas_pix[0:-1]):
                    x = mas_pix[mas_pix[-1] % 3]
                    message += s[x]

    return message


def save_message(message):
    """Сохраняет декодированное сообщение в файл"""
    with open('my_deshifr_message.txt', 'w', encoding='utf-8') as f:
        f.write(message)


def main():
    """Основная функция декодирования"""
    # Загружаем изображение
    image, size = load_image()

    # Декодируем сообщение с замером времени
    stat_t = time.time()
    message = decode_message(image, size)

    # Выводим результаты
    print(f'Время расшифровки: {time.time() - stat_t} сек.')
    print(f'Длина расшифрованного сообщения: {len(message)}')
    print(message)

    # Сохраняем результат
    save_message(message)


if __name__ == "__main__":
    main()