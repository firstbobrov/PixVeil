from cryptography.fernet import Fernet
import base64
import hashlib

def encrypt_with_fernet(message, password):
    """
    Шифрует сообщение с использованием алгоритма Fernet.
    Fernet обеспечивает конфиденциальность, целостность и аутентичность данных.
    
    Args:
        message: строка для шифрования
        password: строка-пароль, используемая для генерации ключа
        
    Returns:
        bytes: зашифрованные данные в формате Fernet
        
    Raises:
        ValueError: если message или password пустые
    """
    if not message or not password:
        raise ValueError("Сообщение и пароль не должны быть пустыми")
    
    # Генерируем ключ из пароля
    key = base64.urlsafe_b64encode(
        hashlib.sha256(password.encode()).digest()
    )
    
    # Создаем шифр и шифруем сообщение
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(message.encode())
    
    return encrypted_data

def decrypt_with_fernet(encrypted_data, password):
    """
    Расшифровывает данные, зашифрованные с помощью encrypt_with_fernet.
    
    Args:
        encrypted_data: bytes, зашифрованные данные от encrypt_with_fernet
        password: строка-пароль, использованная при шифровании
        
    Returns:
        str: расшифрованное сообщение
        
    Raises:
        ValueError: если password пустой или неверный формат данных
        cryptography.fernet.InvalidToken: если пароль неверный или данные повреждены
    """
    if not password:
        raise ValueError("Пароль не должен быть пустым")
    
    # Генерируем тот же ключ из пароля
    key = base64.urlsafe_b64encode(
        hashlib.sha256(password.encode()).digest()
    )
    
    # Создаем шифр и расшифровываем
    cipher = Fernet(key)
    decrypted_message = cipher.decrypt(encrypted_data)
    
    return decrypted_message.decode()

#пример

print(encrypt_with_fernet("секретный текст","секретный ключ"))

s = encrypt_with_fernet("секретный текст","секретный ключ")

print(decrypt_with_fernet(s,"секретный ключ"))
