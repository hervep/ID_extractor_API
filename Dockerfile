FROM python:3.7
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install apt-utils wget build-essential cmake libfreetype6-dev pkg-config libfontconfig-dev libjpeg-dev libopenjp2-7-dev libcairo2-dev libtiff5-dev -y
RUN wget https://poppler.freedesktop.org/poppler-data-0.4.10.tar.gz \
    && tar -xf poppler-data-0.4.10.tar.gz \
    && cd poppler-data-0.4.10 \
    && make install \
    && cd .. \
    && wget https://poppler.freedesktop.org/poppler-21.03.0.tar.xz \
    && tar -xf poppler-21.03.0.tar.xz \
    && cd poppler-21.03.0 \
    && mkdir build \
    && cd build \
    && cmake .. \
    && make \
    && make install \
    && cd ../.. \
    && ldconfig \
    && rm poppler-data-0.4.10.tar.gz \
    && rm -rf poppler-data-0.4.10 \
    && rm poppler-21.03.0.tar.xz \
    && rm -rf poppler-21.03.0
RUN pip install opencv-python-headless
RUN pip install tensorflow==1.14.0
RUN pip install -r requirements.txt
EXPOSE 80
ENV NOM patrick_djakou_Image_ID_Extraction_Docker
CMD ["python3","main.py"]