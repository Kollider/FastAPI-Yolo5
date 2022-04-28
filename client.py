# YOLOv5 🚀 by Ultralytics, GPL-3.0 license
"""
Perform test request
"""
import base64
import io
import pprint

import requests
from PIL import Image

DETECTION_URL = "http://127.0.0.1:8000/upload/"
IMAGE = Image.open('images/zidane.jpg')


def image_to_byte_array(in_image: Image) -> bytes:
	imgByteArr = io.BytesIO()
	in_image.save(imgByteArr, format=in_image.format)
	byteIm = imgByteArr.getvalue()
	return byteIm


bla = image_to_byte_array(IMAGE)

# Read image


response = requests.post(DETECTION_URL, data=bla).json()
img_str = response['1']
img_base64 = base64.b64decode(img_str)
img_bio = io.BytesIO(img_base64)

img = Image.open(img_bio)
img_shape = img.size
#print(type(response['spec']))

# pprint.pprint(response)
