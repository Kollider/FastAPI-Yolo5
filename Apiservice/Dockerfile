FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./pip_wheels/ /code/pip_wheels/
RUN pip install --no-index --find-links /code/pip_wheels/ torch==1.11.0

RUN pip install  -r /code/requirements.txt

#
COPY ./main.py /code/

#
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]