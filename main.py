from flask import Flask, flash,make_response, request, redirect, url_for, render_template,abort,send_file
from werkzeug.utils import secure_filename
import urllib.request
import io
import base64

from extractor import convert_pdf_to_image,get_card_from_image
from PIL import Image
from starlette.responses import StreamingResponse



#import des librairies pour extractor

import os
import sys
import cv2
import numpy as np
from flask_cors import CORS


app = Flask(__name__)
CORS(app)



UPLOAD_FOLDER='./'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf'}

@app.route('/', methods = ['GET'])
def in_api():
    return 'Welcome to ID Card API'

@app.route('/', methods = ['POST'])
def upload_file():

    if 'pdf-file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    f = request.files['pdf-file']
    filename = secure_filename(f.filename)
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    result = convert_pdf_to_image(file_path)

    i = 0
    for page in result:
        indice = str(i)
        name = 'out' + indice + '.png'
        page.save(os.path.join(app.config['UPLOAD_FOLDER'], name))
        i = i + 1

    image = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'],'out0.png'))
    respons = get_card_from_image(image)
    cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'],'save.png'),respons)

    #image = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], 'out1.png'))
    #response = get_card_from_image(image)
    #cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], 'save2.png'), response)

    if os.path.exists('out0.png'):
        os.remove('out0.png')

    if os.path.exists('out1.png'):
        os.remove('out1.png')

    if os.path.exists(file_path):
        os.remove(file_path)

    #return send_file(os.path.join(app.config['UPLOAD_FOLDER'], 'save.png'), mimetype='image/png')
    #return 'done'
    with open(os.path.join(app.config['UPLOAD_FOLDER'], 'save.png'), "rb") as f:
        image_binary = f.read()
        response = make_response(base64.b64encode(image_binary))
        response.headers.set('Content-Type', 'image/png')
        response.headers.set('Content-Disposition', 'attachment', filename='image.png')
        return response





if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0',port=80)