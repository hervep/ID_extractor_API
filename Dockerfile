FROM python:3.9
WORKDIR /app
COPY . /app
RUN python3 -m pip install --upgrade https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.14.0-py3-none-any.whl
RUN pip install -r requirements.txt
ENV NOM Image_ID_Extraction_Docker
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]