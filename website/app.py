from flask import Flask, render_template, request, send_file, redirect, url_for
import os
import base64

app = Flask(__name__)

# Настройка папки для загрузок
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Заглушка для шифрования
def encrypt_image(image_path, message, algorithm, key=None):
    """Заглушка для шифрования - возвращает оригинальное изображение"""
    return image_path


# Заглушка для дешифрования
def decrypt_image(image_path, algorithm, key=None):
    """Заглушка для дешифрования - возвращает тестовое сообщение"""
    return "Результат расшифровки: Пример зашифрованного сообщения. В реальной реализации здесь будет ваш текст."


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/guide')
def guide():
    return render_template('guide.html')


@app.route('/encrypt', methods=['POST'])
def encrypt():
    algorithm = request.form.get('algorithm')
    key = request.form.get('key')
    message = request.form.get('message')
    image = request.files['image']

    if image and image.filename != '':
        filename = image.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(filepath)

        # Обработка изображения (заглушка)
        result_path = encrypt_image(filepath, message, algorithm, key)

        # Преобразуем изображение в base64 для отображения на странице
        with open(result_path, "rb") as img_file:
            b64_string = base64.b64encode(img_file.read()).decode('utf-8')

        return render_template('index.html', encrypted_image=b64_string, mode='encrypt')

    return redirect(url_for('index'))


@app.route('/decrypt', methods=['POST'])
def decrypt():
    algorithm = request.form.get('algorithm')
    key = request.form.get('key')
    image = request.files['image']

    if image and image.filename != '':
        filename = image.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(filepath)

        # Обработка изображения (заглушка)
        result = decrypt_image(filepath, algorithm, key)

        return render_template('index.html', decrypted_result=result, mode='decrypt')

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)