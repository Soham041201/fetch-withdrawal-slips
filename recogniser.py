from imports import *
from constants import *


def preprocess_image(image_path):
    image = cv2.imread(image_path)
    print("THE SHAPE OF THE IMAGE IS")
    image = cv2.resize(image, (1270, 576))
    print(image.shape)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    image = cv2.threshold(
        image, 0, 255, cv2.THRESH_OTSU)[1]
    cv2.imwrite('pre-process.jpg', image)
    return image


def extract_date():
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    # image.source.image_uri = f
    # response = client.text_detection(image=image)

    with io.open('pre-process.jpg', 'rb') as image:
        content = image.read()
        image = vision.Image(content=content)
        response = client.document_text_detection(image=image)

    txt = response.full_text_annotation.text
    result = response.text_annotations

    for i in range(len(result)):
        if (result[i].description in date):
            text, x_min, y_min, x_max, y_max = highlight_text(result[i])
            border_image = generateBox(x_min, y_min, x_max, y_max, text)
            cv2.imwrite('pre-process.jpg', border_image)
            crop_image(x_min, y_min, x_max, y_max, text)

    return txt


def extract_ammount():
    client = vision.ImageAnnotatorClient()
    image = vision.Image()

    with io.open('pre-process.jpg', 'rb') as image:
        content = image.read()
        image = vision.Image(content=content)
        response = client.document_text_detection(image=image)

    txt = response.full_text_annotation.text

    result = response.text_annotations
    for i in range(len(result)):
        if (result[i].description in amount):
            text, x_min, y_min, x_max, y_max = highlight_text(result[i])
            border_image = generateBox(x_min, y_min, x_max, y_max, text)
            cv2.imwrite('pre-process.jpg', border_image)
            crop_image(x_min, y_min, x_max, y_max, text)

    return txt


def extract_signature(file_name):
    # client = vision.ImageAnnotatorClient()
    # image = vision.Image()

    # with io.open('pre-process.jpg', 'rb') as image:
    #     content = image.read()
    #     image = vision.Image(content=content)
    #     response = client.document_text_detection(image=image)

    # txt = response.full_text_annotation.text

    # result = response.text_annotations
    # for i in range(len(result)):
    #     if (result[i].description in signature):
    #         text, x_min, y_min, x_max, y_max = highlight_text(result[i])
    #         border_image = generateBox(x_min, y_min, x_max, y_max, text)
    #         cv2.imwrite('pre-process.jpg', border_image)
    #         # crop_image(x_min, y_min, x_max, y_max, text)
    #         for i in range(len(result)):
    #             if (result[i].description == 'of'):
    #                 text, x_min, y_min, x_max, y_max = highlight_text(
    #                     result[i])
    #                 border_image = generateBox(
    #                     x_min, y_min, x_max, y_max, text)
    #                 cv2.imwrite('pre-process.jpg', border_image)
    #                 if (x_min - x_max < 10):
    #                     border_image = generateBox(
    #                         x_min, y_min, x_max, y_max, text)
    #                     cv2.imwrite('pre-process.jpg', border_image)
    #                     crop_image(x_min, y_min, x_max, y_max, text)
    #                     for i in range(len(result)):
    #                         if (result[i].description == 'Account'):
    #                             text, x_min, y_min, x_max, y_max = highlight_text(
    #                                 result[i])
    #                             border_image = generateBox(
    #                                 x_min, y_min, x_max, y_max, text)
    #                             cv2.imwrite('pre-process.jpg', border_image)
    #                             if (x_min - x_max < 10):
    #                                 border_image = generateBox(
    #                                     x_min, y_min, x_max, y_max, text)
    #                             cv2.imwrite('pre-process.jpg', border_image)
    #                             crop_image(x_min, y_min, x_max, y_max, text)
    #                     for i in range(len(result)):
    #                         if (result[i].description == 'Holder'):
    #                             text, x_min, y_min, x_max, y_max = highlight_text(
    #                                 result[i])
    #                             border_image = generateBox(
    #                                 x_min, y_min, x_max, y_max, text)
    #                             cv2.imwrite('pre-process.jpg', border_image)
    #                             if (x_min - x_max < 10):
    #                                 border_image = generateBox(
    #                                     x_min, y_min, x_max, y_max, text)
    #                             cv2.imwrite('pre-process.jpg', border_image)
    #                             crop_image(x_min, y_min, x_max, y_max, text)

    #                     break
    image = cv2.imread(file_name)


# Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply a threshold to the grayscale image to convert it to a binary image
    _, binary_image = cv2.threshold(
        gray, 0, 255, cv2.THRESH_OTSU)

# Find the contours in the binary image
    contours, _ = cv2.findContours(
        binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Find the largest contour, which should be the signature
    largest_contour = max(contours, key=cv2.contourArea)

# Create a mask for the largest contour
    mask = cv2.drawContours(np.zeros_like(binary_image), [
        largest_contour], 0, 255, -1)
    cv2.imwrite('pre_signature_mask.jpg', mask)

# Extract the signature from the original image using the mask
    signature = cv2.bitwise_and(image, image, mask=mask)
    print("Signature extracted successfully")
    print(file_name)
    cv2.imwrite('pre_signature.jpg', signature)


def extract_account_number():
    client = vision.ImageAnnotatorClient()
    image = vision.Image()

    with io.open('pre-process.jpg', 'rb') as image:
        content = image.read()
        image = vision.Image(content=content)
        response = client.document_text_detection(image=image)
    txt = response.full_text_annotation
    result = response.text_annotations
    for i in range(len(result)):
        if (result[i].description in account):
            text, x_min, y_min, x_max, y_max = highlight_text(result[i])
            border_image = generateBox(x_min, y_min, x_max, y_max, text)
            cv2.imwrite('pre-process.jpg', border_image)
            for i in range(len(result)):
                if (result[i].description in number):
                    text, X_min, Y_min, X_max, Y_max = highlight_text(
                        result[i])
                    border_image = generateBox(
                        X_min, Y_min, X_max, Y_max, text)
                    cv2.imwrite('pre-process.jpg', border_image)
                    print("ACCOUNT NUMBER")
                    print("Account")
                    print(X_min, Y_min, X_max, Y_max)
                    print("Number")
                    print(x_min, y_min, x_max, y_max)
                    if (X_min - x_max < 10):
                        border_image = generateBox(
                            x_min, Y_min, X_max, Y_max, text)
                        cv2.imwrite('pre-process.jpg', border_image)
                        crop_image(x_min, Y_min, X_max, Y_max, text)
                        break

    return txt


def highlight_text(result):
    cord_df = pd.DataFrame(columns=['x', 'y'])

    coordinates = result.bounding_poly.vertices
    for vertex in coordinates:
        cord_df = cord_df.append(
            {'x': vertex.x, 'y': vertex.y}, ignore_index=True)

    x_min, y_min = np.min(cord_df['x']), np.min(cord_df['y'])
    x_max, y_max = np.max(cord_df['x']), np.max(cord_df['y'])
    return result.description, x_min, y_min, x_max, y_max


def generateBox(x_min, y_min, x_max, y_max, text):
    img = cv2.imread('pre-process.jpg')
    img = cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 1)
    return img


def crop_image(x_min, y_min, x_max, y_max, text):
    from PIL import Image
    img = Image.open('pre-process.jpg')
    if (text in date):
        try:
            cropped_image = img.crop(
                (x_min+40, y_min-5, x_max+160, y_max+5))
            cropped_image.save('date.jpg')
        except Exception as e:
            print("Error in date")
            print(e)
    elif (text in amount):
        try:

            cropped_image = img.crop(
                (x_min+20, y_min, x_max+200, y_max))
            cropped_image.save('amount.jpg')
        except Exception as e:
            print("Error in amount")
            print(e)
    elif (text in number):
        try:
            cropped_image = img.crop(
                (x_min-200, y_min+20, x_max+200, y_max+50))
            cropped_image.save('account_number.jpg')
        except Exception as e:
            print("Error in account number")
            print(e)
    elif (text in signature):
        try:
            cropped_image = img.crop(
                (x_min, y_min-200, x_max+100, y_max))
            cropped_image.save('signature.jpg')
        except Exception as e:
            print("Error in signature")
            print(e)


def detect_reference_image(ref_img, img):
    val = 0
    try:
        gray_ref = cv2.cvtColor(ref_img, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(img, gray_ref, cv2.TM_CCOEFF_NORMED)
        if result is not None:
            _, max_val, _, max_loc = cv2.minMaxLoc(result)
            print(max_val)
            if max_val >= 0.6:
                if max_val > val:
                    val = max_val
                    logo = img
                x, y = max_loc
                h, w, _ = ref_img.shape
                from PIL import Image
                image = Image.open('pre-process.jpg')
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cropped_image = image.crop((x, y, x+w, y+h))
                cropped_image.save(img + 'logo.jpg')
        return max_val
    except Exception as e:
        print("Error in detect_reference_image")
        print(e)
        return 0
    print(max_val)
