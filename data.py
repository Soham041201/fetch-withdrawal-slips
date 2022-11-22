from imports import *
from recogniser import *


def get_data(file_name):
    preprocess_image(file_name)
    
    extract_date()
    extract_ammount()
    extract_account_number()
    print("Final Resultss")
    date = preprocess_data('date.jpg','pre_date.jpg')
    print("Date: ",date)
    ammount = preprocess_data('amount.jpg','pre_ammount.jpg')
    print("Ammount: ",ammount)
    acc_number = preprocess_data('account_number.jpg','pre_account_number.jpg')
    print("Account Number: ",acc_number)
    return date,ammount,acc_number
    
    

def preprocess_data(image_path,name):
    image = cv2.imread(image_path)
    cv2.imwrite(name, image)
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    with io.open(name, 'rb') as image:
        content = image.read()
        image = vision.Image(content=content)
        response = client.document_text_detection(image=image)
    result = response.full_text_annotation.text
    return result 

