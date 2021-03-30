FROM python:3.9
WORKDIR /app
COPY . /app
RUN pip install opencv-python-headless
RUN pip install --ignore-installed --upgrade https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-1.14.0-cp35-cp35m-linux_x86_64.whl 
RUN pip install -r requirements.txt
ENV NOM Image_ID_Extraction_Docker
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
