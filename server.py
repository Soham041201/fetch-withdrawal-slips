from flask import Flask, jsonify, request
from recogniser import *
from imports import *
from data import *
app = Flask(__name__)


@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():

    res = requests.get("https://imgs.search.brave.com/gV1lY-KnhVa-vQjqB6VH6O5A2k67Dh_B28jRTYk-ues/rs:fit:1200:720:1/g:ce/aHR0cHM6Ly9pLnl0/aW1nLmNvbS92aS80/QndkZlVUbVJ3TS9t/YXhyZXNkZWZhdWx0/LmpwZw", stream=True)
    file_name = "test.jpg"
    if res.status_code == 200:
        with open(file_name, 'wb') as f:
            shutil.copyfileobj(res.raw, f)
            print('Image sucessfully Downloaded: ', file_name)
    else:
        print('Image Couldn\'t be retrieved')

    date, ammount, acc_number = get_data(file_name)

    return jsonify({'date': date, 'ammount': ammount, 'acc_number': acc_number})


@app.route('/add', methods=['POST'])
def get_data_from_image():
    dataDict = request.get_json()
    link = dataDict['image_link']
    res = requests.get(link, stream=True)
    file_name = "test.jpg"
    if res.status_code == 200:
        with open(file_name, 'wb') as f:
            shutil.copyfileobj(res.raw, f)
            print('Image sucessfully Downloaded: ', file_name)
    else:
        print('Image Couldn\'t be retrieved')
    date, ammount, acc_number = get_data(file_name)
    return jsonify({'date': date, 'ammount': ammount, 'acc_number': acc_number})


if __name__ == '__main__':
    app.run()
