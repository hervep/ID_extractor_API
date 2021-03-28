#from fastapi import FastAPI, File, HTTPException, UploadFile
from io import BytesIO
from typing import List
import uvicorn
from fastapi import FastAPI, File, HTTPException, UploadFile
from extractor import convert_pdf_to_image,get_card_from_image
from PIL import Image
from pydantic import BaseModel

#import des librairies pour extractor

import os
import sys
import cv2
import numpy as np

app = FastAPI()


@app.post("/get_card_from_image")
async def extract(file: UploadFile = File(...)):
    # Ensure that the file is an image
    if not file.content_type.startswith("application/"):
        raise HTTPException(status_code=400, detail="File provided is not an pdf.")
    #content = await file.read()
    result = convert_pdf_to_image(file.filename)

    i = 0
    for page in result:
        indice = str(i)
        page.save('out' + indice + '.JPG', 'JPEG')
        i = i + 1

    image = cv2.imread('out0.jpg')
    response = get_card_from_image(image)
    cv2.imwrite("cropped_card.jpg", response)

    if os.path.exists('out0.jpg'):
        os.remove('out0.jpg')

    if os.path.exists('out1.jpg'):
        os.remove('out1.jpg')

    return 'Done'
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000)