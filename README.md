# FastAPI-Yolo5
FastAPI server with Yolov5 detect

# Development
This document assumes that all commands are executed within `Apiservice` project directory.  
In order to do so, please type `cd Apiservice` once before running anything else.

## Installing requirements

`pip install -r requirements.txt`

## Server setup

`docker build -t backend .`  
`docker run -p 8000:8000 backend`

## Client usage

`python client.py --source zidane.jpg`
