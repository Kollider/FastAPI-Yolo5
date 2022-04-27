import uvicorn
from fastapi import FastAPI, UploadFile, File

app = FastAPI()


def save_file(filename, data):
	with open(filename, 'wb') as f:
		f.write(data)


@app.get("/")
async def home():
	return {"message": "Hello World"}


@app.post("/upload")
async def image_process(file: UploadFile = File(...)):
	contents = await file.read()
	save_file(file.filename, contents)
	return {"Filename": file.filename}


if __name__ == '__main__':
	uvicorn.run(app, host='127.0.0.1', port=8000, debug=True)
