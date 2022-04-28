"""import requests

url = 'http://127.0.0.1:8000/upload'
file = {'file': open('images/zidane.jpg', 'rb')}
resp = requests.post(url=url, files=file)
print(resp.json())
"""
import io
from PIL import Image

im = Image.open('images/zidane.jpg')


def image_to_byte_array(image: Image) -> bytes:
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format=image.format)
  byteIm = imgByteArr.getvalue()
  return byteIm

bla = image_to_byte_array(im)

image = Image.open(io.BytesIO(bla))

image.show()