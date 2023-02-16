from imports import *
from recogniser import *


def get_data(file_name):
    image = preprocess_image(file_name)
    # extract_date()
    # extract_ammount()
    # extract_account_number()
    extract_signature(file_name)
    logo = '' 
    # from PIL import Image
    # img = Image.open('pre-process.jpg')
    # root_dir = '/Users/sohamsattigeri/Soham/College/EDI/fetch-withdrawal-slips/logos'
    # temp = 0
    # for subdir, dirs,files in os.walk(root_dir):
    #     for file in files:
    #         file_path = os.path.join(subdir, file)
    #         print("Path of the logo")
    #         print(file_path)
    #         ref_img = cv2.imread(file_path)
    #         ref_img = cv2.resize(ref_img, (100,100)) 
    #         print("Path of the logo")
    #         print(file_path)
    #         max_val = detect_reference_image(ref_img, image)
    #         if max_val > temp: 
    #             temp = max_val
    #             logo = file_path
            
            
    date = preprocess_data('date.jpg','pre_date.jpg')
    ammount = preprocess_data('amount.jpg','pre_ammount.jpg')
    acc_number = preprocess_data('account_number.jpg','pre_account_number.jpg')
    return date,ammount,acc_number, logo

    

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

