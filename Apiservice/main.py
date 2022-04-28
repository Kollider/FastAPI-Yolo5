# YOLOv5 🚀 by Ultralytics, GPL-3.0 license
"""
Run a Flask REST API exposing a YOLOv5s model
"""

import argparse
import base64
import io

import torch
import uvicorn
from fastapi import FastAPI, Depends, Request
from PIL import Image

app = FastAPI()

DETECTION_URL = "/upload"


async def parse_body(request: Request):
	data: bytes = await request.body()
	return data


def image_to_byte_array(in_image: Image) -> bytes:
	imgByteArr = io.BytesIO()
	in_image.save(imgByteArr, format=in_image.format)
	byteIm = imgByteArr.getvalue()
	return byteIm


@app.post(DETECTION_URL)
async def image_process(data: bytes = Depends(parse_body)):
	image_bytes = data
	image = Image.open(io.BytesIO(image_bytes))
	results = model(image)
	tdict = {}
	i = 1
	for img in results.imgs:
		# tdict['spec']=img
		print(results)
		print(img)

	results.render()

	for img in results.imgs:
		buffered = io.BytesIO()
		img_base64 = Image.fromarray(img)
		img_base64.save(buffered, format="JPEG")
		img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')  # base64 encoded image with results
		tdict[f'{i}'] = img_str
	# bla = image_to_byte_array(Image.open('runs/de'))
	# tdict['additional']=results.pandas().xyxy[0].to_json(orient="records")

	return tdict  # results.pandas().xyxy[0].to_json(orient="records")


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Flask API exposing YOLOv5 model")
	parser.add_argument("--port", default=8000, type=int, help="port number")
	opt = parser.parse_args()

	# Fix known issue urllib.error.HTTPError 403: rate limit exceeded https://github.com/ultralytics/yolov5/pull/7210
	torch.hub._validate_not_a_forked_repo = lambda a, b, c: True

	model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True, force_reload=False)
	uvicorn.run(app, host="127.0.0.1", port=opt.port)  # debug=True causes Restarting with stat
