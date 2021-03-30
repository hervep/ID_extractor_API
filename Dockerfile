FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7-slim
WORKDIR /app
COPY . /app
RUN pip install opencv-python-headless
RUN pip install tensorflow==1.14.0
RUN pip install -r requirements.txt
ENV NOM Image_ID_Extraction_Docker
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
