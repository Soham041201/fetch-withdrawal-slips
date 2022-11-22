from imports import *


def preprocess_image(image_path):
    image = cv2.imread(image_path)

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
        if (result[i].description == "Date" or result[i].description == "date" or result[i].description == "DATE" or result[i].description == "Dated" or result[i].description == "dated" or result[i].description == "DATED"):
            text, x_max, x_min, y_max, y_min = highlight_text(result[i])
            border_image = generateBox(x_min, y_min, x_max, y_max, text)
            cv2.imwrite('test.jpg', border_image)
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
        if (result[i].description == "Rs" or result[i].description == "₹" or result[i].description == "INR"):
            text, x_max, x_min, y_max, y_min = highlight_text(result[i])
            border_image = generateBox(x_min, y_min, x_max, y_max, text)
            cv2.imwrite('test.jpg', border_image)
            crop_image(x_min, y_min, x_max, y_max, text)

    return txt


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
        if (result[i].description == "ACCOUNT"):
            text, x_max, x_min, y_max, y_min = highlight_text(result[i])
            border_image = generateBox(x_min, y_min, x_max, y_max, text)

            for i in range(len(result)):
                if (result[i].description == "Number" or result[i].description == "NUMBER" or result[i].description == "number"):
                    text, X_max, X_min, Y_max, Y_min = highlight_text(
                        result[i])
                    if (x_min - X_min < 4):
                        border_image = generateBox(
                            X_min, Y_min, x_max, Y_max, text)
                        cv2.imwrite('test.jpg', border_image)
                        crop_image(X_min, Y_min, x_max, Y_max, text)
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
    img = cv2.imread('test.jpg')
    img = cv2.rectangle(img, (y_max, x_min), (x_max, y_min), (0, 255, 0), 1)
    return img


def crop_image(x_min, y_min, x_max, y_max, text):
    from PIL import Image
    img = Image.open('test.jpg')

    if (text == "Date" or text == "date" or text == "DATE" or text == "Dated" or text == "dated" or text == "DATED"):
        cropped_image = img.crop(
            (x_max, x_min-30, y_max+(y_max*0.6), y_min+30))
        cropped_image.save('date.jpg')
    elif (text == "Rs" or text == "₹" or text == "INR"):
        cropped_image = img.crop(
            (x_max, x_min-30, y_max+(y_max*0.6), y_min+30))
        cropped_image.save('amount.jpg')
    elif (text == "Number" or text == "NUMBER" or text == "number" or text == "No." or text == "NO." or text == "no."):
        cropped_image = img.crop(
            (x_max-30, x_min, y_max*1.6, y_min+(y_min*0.5)))
        cropped_image.save('account_number.jpg')
