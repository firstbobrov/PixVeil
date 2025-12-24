def encode_message(message, char_set):
    """
    Кодирует сообщение в массив индексов символов в char_set.
    
    Args:
        message: строка для кодирования
        char_set: список символов (алфавит)
        
    Returns:
        list: массив индексов символов в char_set
        
    Raises:
        ValueError: если символ из сообщения не найден в char_set
    """
    char_to_index = {char: idx for idx, char in enumerate(char_set)}
    encoded = []
    
    for char in message:
        if char in char_to_index:
            encoded.append(char_to_index[char])
        else:
            raise ValueError(f"Символ '{char}' не найден в char_set")
    
    return encoded


def decode_message(mass, char_set):
    """
    Декодирует массив индексов обратно в строку.
    
    Args:
        mass: список индексов для декодирования
        char_set: список символов (алфавит)
        
    Returns:
        str: декодированная строка
        
    Raises:
        IndexError: если индекс выходит за пределы char_set
    """
    decoded_chars = []
    
    for idx in mass:
        if 0 <= idx < len(char_set):
            decoded_chars.append(char_set[idx])
        else:
            raise IndexError(f"Индекс {idx} выходит за пределы char_set (длина: {len(char_set)})")
    
    return ''.join(decoded_chars)
#пример
s = ['ь', '|', 'у', 'т', 't', 'щ', 'А', 'Х', 'Д', '6', 'с', 'Ж',
     '#', 'К', 'g', '1', '5', 'b', '}', 'n', 'ц', 'з', 'Г', 's',
     'w', '/', 'Й', ';', 'п', '\n', 'р', 'Ч', 'ф', '>', '7', '_',
     'е', 'л', 'F', 'O', 'V', 'a', '.', '+', 'o', ']', 'i', 'Э',
     'ё', '=', '9', 'Н', 'z', 'K', '^', 'С', '2', 'и', 'I', 'Y',
     'Т', 'Q', 'X', 'q', 'Ъ', 'y', '%', 'R', 'Р', 'З', '?', '`',
     'v', 'L', '\t', '*', 'б', 'k', 'У', 'e', 'p', 'H', 'Ц', '-',
     'Щ', '&', 'U', 'P', 'f', 'х', 'Л', 'В', '8', 'а', 'Ё', ')',
     'я', 'д', '<', '"', 'Ю', 'к', '[', 'G', 'э', 'j', 'B', 'ы',
     'Я', '@', 'T', 'M', 'ч', 'l', 'ш', '!', 'Z', 'О', 'd', '(',
     'x', 'г', '$', 'C', ' ', ':', 'ж', 'ю', 'Ы', 'Ф', 'E', '\r',
     'c', '0', 'Б', 'м', 'н', 'И', 'A', ',', '\\', 'D', 'М', 'N',
     'Ш', 'm', 'S', 'в', '{', "'", 'П', 'й', 'W', 'о', 'Е', 'J',
     '4', 'Ь', '~', '3', 'r', 'h', 'u', 'ъ']


print(encode_message("Когда то мы были интенсионал футуризма...",s))
enc = encode_message("Когда то мы были интенсионал футуризма...",s)
print(decode_message(enc,s))
