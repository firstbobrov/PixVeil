import os
import uuid
import base64
from flask import Flask, render_template, request, redirect, url_for, flash, session
from encryption_utils import (
    base_encrypt, base_decrypt, base_max_message_length,
    modified_encrypt, modified_decrypt, modified_max_message_length
)

# ⚠️ Убедитесь, что файл переименован в optional_cipher.py
try:
    from optional_cipher import encrypt_with_fernet, decrypt_with_fernet
except ImportError:
    raise ImportError("Не найден файл optional_cipher.py. Переименуйте optional_cipher(Fernet).py в optional_cipher.py")

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'supersecretkey')
BASE_DIR = '/data' if os.path.exists('/data') else os.getcwd()
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
app.config['RESULT_FOLDER'] = os.path.join(BASE_DIR, 'results')
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/tool')
def tool():
    encrypt_result_id = request.args.get('encrypt_result')
    encrypt_info = session.pop('encrypt_info', None)
    mode = request.args.get('mode', 'encrypt')
    
    if encrypt_result_id:
        result_path = os.path.join(app.config['RESULT_FOLDER'], f'{encrypt_result_id}.png')
        if os.path.exists(result_path):
            with open(result_path, 'rb') as f:
                b64_string = base64.b64encode(f.read()).decode('utf-8')
            os.remove(result_path)
            return render_template('tool.html', encrypted_image=b64_string, mode='encrypt', encrypt_info=encrypt_info)

    decrypt_result = session.pop('decrypt_result', None)
    if decrypt_result:
        return render_template('tool.html', decrypted_result=decrypt_result, mode='decrypt')

    return render_template('tool.html', mode=mode)

@app.route('/guide')
def guide():
    return render_template('guide.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    algorithm = request.form.get('algorithm')
    message = request.form.get('message', '')
    image = request.files.get('image')
    key = request.form.get('key', '').strip()  # Получаем ключ из формы

    if not image or image.filename == '':
        flash('Не выбран файл изображения', 'danger')
        return redirect(url_for('tool'))

    if not message:
        flash('Введите сообщение для шифрования', 'danger')
        return redirect(url_for('tool'))

    use_fernet = bool(key)  # 🔹 Булевый флаг: шифруем ли с ключом
    message_to_hide = message

    # 1️⃣ Предварительное шифрование Fernet, если ключ указан
    if use_fernet:
        try:
            fernet_token = encrypt_with_fernet(message, key)
            message_to_hide = fernet_token.decode('utf-8')  # Fernet возвращает bytes, переводим в строку для стеганографии
        except Exception as e:
            flash(f'Ошибка шифрования ключом: {str(e)}', 'danger')
            return redirect(url_for('tool'))

    input_ext = os.path.splitext(image.filename)[1]
    if input_ext.lower() not in ['.png', '.jpg', '.jpeg']:
        flash('Поддерживаются только форматы PNG и JPG', 'danger')
        return redirect(url_for('tool'))

    uid = uuid.uuid4().hex
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{uid}_input{input_ext}')
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{uid}_output.png')
    image.save(input_path)

    max_len = 0
    try:
        if algorithm == 'base':
            max_len = base_max_message_length(input_path)
            success, written = base_encrypt(input_path, output_path, message_to_hide)
            message_bytes = message_to_hide.encode('utf-8')
            written_symbols = len(message_bytes[:written].decode('utf-8', errors='ignore'))
            unit = 'байт'
            written_units = written
        elif algorithm == 'modified':
            max_len = modified_max_message_length(input_path)
            success, written = modified_encrypt(input_path, output_path, message_to_hide)
            written_symbols = written
            unit = 'символов'
            written_units = written
        else:
            flash('Неизвестный алгоритм', 'danger')
            return redirect(url_for('tool'))

        # 2️⃣ Строгая проверка вместимости для режима с ключом
        if use_fernet and not success:
            flash('Не удалось зашифровать сообщение с ключом: оно не помещается в изображение. Уменьшите сообщение или используйте изображение большего размера.', 'danger')
            return redirect(url_for('tool'))

        total_symbols = len(message)
        encrypt_info = {
            'success': success,
            'written_symbols': written_symbols,
            'total_symbols': total_symbols,
            'written_units': written_units,
            'unit': unit,
            'max_len': max_len if not use_fernet else 0,  # При use_fernet длину не показываем
            'algorithm': 'Базовый' if algorithm == 'base' else 'Модифицированный',
            'use_fernet': use_fernet  # 🔹 Сохраняем флаг в сессии
        }
        session['encrypt_info'] = encrypt_info

        if not success and not use_fernet:
            flash(f'Не удалось зашифровать всё сообщение. Зашифровано только {written_symbols} из {total_symbols} символов.', 'warning')
        else:
            flash('Изображение успешно зашифровано!', 'success')

        result_id = uuid.uuid4().hex
        result_path = os.path.join(app.config['RESULT_FOLDER'], f'{result_id}.png')
        os.rename(output_path, result_path)
        return redirect(url_for('tool', encrypt_result=result_id))

    except Exception as e:
        flash(f'Ошибка при шифровании: {str(e)}', 'danger')
        return redirect(url_for('tool'))
    finally:
        for path in [input_path, output_path]:
            if os.path.exists(path):
                try: os.remove(path)
                except: pass

@app.route('/decrypt', methods=['POST'])
def decrypt():
    algorithm = request.form.get('algorithm')
    image = request.files.get('image')
    key = request.form.get('key', '').strip()
    use_fernet = bool(key)

    if not image or image.filename == '':
        flash('Не выбран файл изображения', 'danger')
        return redirect(url_for('tool'))

    input_ext = os.path.splitext(image.filename)[1]
    if input_ext.lower() not in ['.png', '.jpg', '.jpeg']:
        flash('Поддерживаются только форматы PNG и JPG', 'danger')
        return redirect(url_for('tool'))

    uid = uuid.uuid4().hex
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{uid}_input{input_ext}')
    image.save(input_path)

    try:
        if algorithm == 'base':
            extracted_msg = base_decrypt(input_path)
        elif algorithm == 'modified':
            extracted_msg = modified_decrypt(input_path)
        else:
            flash('Неизвестный алгоритм', 'danger')
            return redirect(url_for('tool'))

        if not extracted_msg:
            raise Exception('Не удалось извлечь сообщение из изображения')

        # 3️⃣ Расшифровка Fernet после извлечения, если был ключ
        if use_fernet:
            try:
                final_message = decrypt_with_fernet(extracted_msg.encode('utf-8'), key)
            except Exception as e:
                flash('Ошибка расшифровки: неверный ключ или повреждённые данные.', 'danger')
                return redirect(url_for('tool'))
        else:
            final_message = extracted_msg

        flash('Сообщение успешно расшифровано!', 'success')
        return render_template('tool.html', decrypted_result=final_message, mode='decrypt')

    except Exception as e:
        flash(f'Ошибка при дешифровании: {str(e)}', 'danger')
        return redirect(url_for('tool'))
    finally:
        if os.path.exists(input_path):
            try: os.remove(input_path)
            except: pass

@app.route('/health')
def health():
    return {'status': 'ok'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
