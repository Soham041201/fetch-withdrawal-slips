from flask import Flask, jsonify, request
from recogniser import *
from imports import *
from data import *
app = Flask(__name__)


@app.route('/')
def hello_world():
    root_dir = '/Users/sohamsattigeri/Soham/College/EDI/fetch-withdrawal-slips/test_images'
    # date, ammount, acc_number, logo = get_data('/Users/sohamsattigeri/Soham/College/EDI/fetch-withdrawal-slips/test_images/9.jpg')
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(subdir, file)
            print(file_path)
            date, ammount, acc_number, logo, signatureFile = get_data(
                file_path)
            print(file_path)
            print(date, ammount, acc_number)
            from csv import writer
            try:
                fDate = int(''.join(filter(str.isdigit, date)))
                fDate = str(fDate)
                fDate = fDate[0:2] + '-' + fDate[2:4] + '-' + fDate[-4:]
                if (fDate.count('-') == 1):
                    fDate = '0' + fDate
                date = fDate
            except:
                date = '-'
            try:
                fAmmount = int(''.join(filter(str.isdigit, ammount)))
                ammount = fAmmount
            except:
                ammount = '-'
            try:
                fAcc = int(''.join(filter(str.isdigit, acc_number)))
                acc_number = fAcc
            except:
                acc_number = '-'

            List = [date, ammount, acc_number, logo, signatureFile]
            with open('result.csv', 'a') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow(List)
            f_object.close()
    df = pd.read_csv("result.csv", header="Bank Withdrawal Slip Data")
    df = df.rename(columns={0: "Date", 1: "Ammount",
                   2: "Account Number", 3: "Logo", 4: "Signature"})
    df.to_csv("result.csv", index=False)
    f_object.close()
    return jsonify({'date': date, 'ammount': ammount, 'acc_number': acc_number})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
