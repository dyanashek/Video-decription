from functions import describe_image, save_random_frame

import os
import uuid

from flask import Flask, render_template, request


app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html', description = 'После загрузки видео из него будет выбран случайный кадр, нейросеть составит по нему историю.')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('index.html', description = 'Файл не выбран')

    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', description = 'Файл не выбран')

    if file:
        extension = file.filename.split('.')[-1]
        file_name = str(uuid.uuid4())
        file.save(f'{file_name}.{extension}')

        try:
            save_random_frame(f'{file_name}.{extension}', f'{file_name}.jpeg')
            os.remove(f'{file_name}.{extension}')
        except:
            return render_template('index.html', description = 'Неизвестная ошибка.')

        result = describe_image(f'{file_name}.jpeg')
        os.remove(f'{file_name}.jpeg')

        return render_template('index.html', description = result)



if __name__ == '__main__':
    app.run(debug=True)