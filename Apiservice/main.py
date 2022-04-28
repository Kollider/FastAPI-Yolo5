import argparse
import base64
import io
import json
import torch
import uvicorn

from fastapi import FastAPI, Depends, Request
from PIL import Image

app = FastAPI()

DETECTION_URL = "/upload"


# convert image to bytes
def image_to_byte_array(in_image: Image) -> bytes:
	imgByteArr = io.BytesIO()
	in_image.save(imgByteArr, format=in_image.format)
	byteIm = imgByteArr.getvalue()  # image in bytes
	return byteIm


# get image bytes from request
async def parse_body(request: Request):
	data: bytes = await request.body()
	return data


@app.post(DETECTION_URL)
async def image_process(image_bytes: bytes = Depends(parse_body)):
	image = Image.open(io.BytesIO(image_bytes))
	results = model(image)

	detect_res = results.pandas().xyxy[0].to_json(orient="records")  # bound box info to json format using pandas
	detect_res_json = json.loads(detect_res)

	response_dict = {
		'bound_box_info': detect_res_json
	}

	results.render()

	imgByteArr = io.BytesIO()
	img_base64 = Image.fromarray(results.imgs[0])  # Get Pillow image
	img_base64.save(imgByteArr, format="JPEG")
	img_str = base64.b64encode(imgByteArr.getvalue()).decode('utf-8')  # base64 encoded image with results
	response_dict['image'] = img_str  # write image to response

	return response_dict


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Flask API exposing YOLOv5 model")
	parser.add_argument("--port", default=8000, type=int, help="port number")
	opt = parser.parse_args()

	# Fix known issue urllib.error.HTTPError 403: rate limit exceeded https://github.com/ultralytics/yolov5/pull/7210
	torch.hub._validate_not_a_forked_repo = lambda a, b, c: True

	model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True, force_reload=False)
	uvicorn.run(app, host="127.0.0.1", port=opt.port)  # debug=True causes Restarting with stat
