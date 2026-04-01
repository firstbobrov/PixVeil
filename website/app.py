import os
import uuid
import base64
from flask import Flask, render_template, request, redirect, url_for, flash, session
from encryption_utils import (
    base_encrypt, base_decrypt, base_max_message_length,
    modified_encrypt, modified_decrypt, modified_max_message_length
)

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Замените на надёжный ключ в продакшене
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
app.config['RESULT_FOLDER'] = 'results'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)


@app.route('/')
def index():
    encrypt_result_id = request.args.get('encrypt_result')
    if encrypt_result_id:
        result_path = os.path.join(app.config['RESULT_FOLDER'], f'{encrypt_result_id}.png')
        if os.path.exists(result_path):
            with open(result_path, 'rb') as f:
                b64_string = base64.b64encode(f.read()).decode('utf-8')
            os.remove(result_path)
            return render_template('index.html', encrypted_image=b64_string, mode='encrypt')

    decrypt_result = session.pop('decrypt_result', None)
    if decrypt_result:
        return render_template('index.html', decrypted_result=decrypt_result, mode='decrypt')

    return render_template('index.html')


@app.route('/guide')
def guide():
    return render_template('guide.html')


@app.route('/encrypt', methods=['POST'])
def encrypt():
    algorithm = request.form.get('algorithm')
    message = request.form.get('message')
    image = request.files.get('image')

    if not image or image.filename == '':
        flash('Не выбран файл изображения', 'danger')
        return redirect(url_for('index'))

    if not message:
        flash('Введите сообщение для шифрования', 'danger')
        return redirect(url_for('index'))

    uid = uuid.uuid4().hex
    input_ext = os.path.splitext(image.filename)[1]
    if input_ext.lower() not in ['.png', '.jpg', '.jpeg']:
        flash('Поддерживаются только форматы PNG и JPG', 'danger')
        return redirect(url_for('index'))

    input_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{uid}_input{input_ext}')
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{uid}_output.png')
    image.save(input_path)

    # Проверка максимальной длины сообщения
    max_len = 0
    if algorithm == 'base':
        max_len = base_max_message_length(input_path)
    elif algorithm == 'modified':
        max_len = modified_max_message_length(input_path)

    if max_len > 0 and len(message) > max_len:
        flash(f'Сообщение слишком длинное. Максимальная длина для выбранного алгоритма и этого изображения: {max_len} символов.', 'warning')
        if os.path.exists(input_path):
            os.remove(input_path)
        return redirect(url_for('index'))

    try:
        if algorithm == 'base':
            success, written = base_encrypt(input_path, output_path, message)
        elif algorithm == 'modified':
            success, written = modified_encrypt(input_path, output_path, message)
        else:
            flash('Неизвестный алгоритм', 'danger')
            return redirect(url_for('index'))

        if not success:
            flash(f'Не удалось зашифровать всё сообщение. Зашифровано только {written} из {len(message)} символов. Попробуйте использовать изображение большего размера.', 'warning')
        else:
            flash('Изображение успешно зашифровано!', 'success')

        result_id = uuid.uuid4().hex
        result_path = os.path.join(app.config['RESULT_FOLDER'], f'{result_id}.png')
        os.rename(output_path, result_path)
        return redirect(url_for('index', encrypt_result=result_id))

    except Exception as e:
        flash(f'Ошибка при шифровании: {str(e)}', 'danger')
        return redirect(url_for('index'))

    finally:
        for path in [input_path, output_path]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except:
                    pass


@app.route('/decrypt', methods=['POST'])
def decrypt():
    algorithm = request.form.get('algorithm')
    image = request.files.get('image')

    if not image or image.filename == '':
        flash('Не выбран файл изображения', 'danger')
        return redirect(url_for('index'))

    uid = uuid.uuid4().hex
    input_ext = os.path.splitext(image.filename)[1]
    if input_ext.lower() not in ['.png', '.jpg', '.jpeg']:
        flash('Поддерживаются только форматы PNG и JPG', 'danger')
        return redirect(url_for('index'))

    input_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{uid}_input{input_ext}')
    image.save(input_path)

    try:
        if algorithm == 'base':
            result = base_decrypt(input_path)
        elif algorithm == 'modified':
            result = modified_decrypt(input_path)
        else:
            flash('Неизвестный алгоритм', 'danger')
            return redirect(url_for('index'))

        if not result:
            raise Exception('Не удалось извлечь сообщение из изображения')

        session['decrypt_result'] = result
        flash('Сообщение успешно расшифровано!', 'success')
        return redirect(url_for('index'))

    except Exception as e:
        flash(f'Ошибка при дешифровании: {str(e)}', 'danger')
        return redirect(url_for('index'))

    finally:
        if os.path.exists(input_path):
            try:
                os.remove(input_path)
            except:
                pass


if __name__ == '__main__':
    app.run(debug=True)