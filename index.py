from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import face_recognition
import numpy as np
from io import BytesIO
from PIL import Image

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/detect-faces/")
def indentify_face():
    image = face_recognition.load_image_file("images/face.jpg")
    face_locations = face_recognition.face_locations(image)
    return {"face_locations": face_locations}

@app.get("/")
async def root():
    return {"message": "Face Recognition API is running"}