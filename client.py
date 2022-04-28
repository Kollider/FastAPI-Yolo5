import base64
import io
import requests

from PIL import Image

import pandas as pd

DETECTION_URL = "http://127.0.0.1:8000/upload/"
IMAGE = Image.open('images/zidane.jpg')


def image_to_byte_array(in_image: Image) -> bytes:
	imgByteArr = io.BytesIO()
	in_image.save(imgByteArr, format=in_image.format)
	byteIm = imgByteArr.getvalue()
	return byteIm


img_bytes = image_to_byte_array(IMAGE)  # convert image to bytes
response = requests.post(DETECTION_URL, data=img_bytes).json()  # send image to detect

img_str = response['image']  # get image in base64 string format after detecting
img_base64 = base64.b64decode(img_str)  # convert base64 string to bytes
img_bio = io.BytesIO(img_base64)  # Convert to BytesIO to be handled by Pillow

img = Image.open(img_bio)  # Open with Pilllow
img.save('output.png', format='png')  # save image with bounding boxes

special_info = response['bound_box_info']  # information about bounding boxes

df = pd.DataFrame.from_dict(special_info)  # create dataframe from dictionary
df.to_csv(r'bound_boxes.csv', index=False, header=True)  # write to csv
