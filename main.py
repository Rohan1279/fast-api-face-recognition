import shutil
from typing import List
from time import time
from fastapi import FastAPI, __version__
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your needs
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],
)

import face_recognition
import cv2
import shutil
import os
from PIL import Image, ImageDraw

app.mount("/known_faces", StaticFiles(directory="known_faces"), name="known_faces")

def read_img(path, resize=True):
    img = cv2.imread(path)
    if resize:
        (h, w) = img.shape[:2]
        width = 800  # Increased width for better face detection
        ratio = width / float(w)
        height = int(h * ratio)
        img = cv2.resize(img, (width, height))
    return img

def preprocess_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply histogram equalization
    equalized = cv2.equalizeHist(gray)
    # Convert back to BGR
    preprocessed = cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)
    return preprocessed

def detect_faces(image_path, resize=True):
    image = read_img(image_path, resize)
    preprocessed_image = preprocess_image(image)
    face_locations = face_recognition.face_locations(preprocessed_image)
    face_encodings = face_recognition.face_encodings(preprocessed_image, face_locations)
    return face_locations, face_encodings, image

def process_input_folder(input_dir, known_faces_dir):
    known_faces = {}
    face_label_counter = 1
    face_urls = []

    for image_name in os.listdir(input_dir):
        image_path = os.path.join(input_dir, image_name)
        print(f"Processing {image_name}")

        face_locations, face_encodings, image = detect_faces(image_path)

        if not face_encodings:
            print(f"No faces detected in resized image of {image_name}, trying original image")
            face_locations, face_encodings, image = detect_faces(image_path, resize=False)

        if not face_encodings:
            print(f"No faces detected in original image of {image_name}")
            continue

        for i, face_encoding in enumerate(face_encodings):
            is_new_face = True
            for label, known_encoding in known_faces.items():
                face_distance = face_recognition.face_distance([known_encoding], face_encoding)
                if face_distance < 0.5:  # Lowered threshold for stricter matching
                    is_new_face = False
                    break

            if is_new_face:
                label = f"face_{face_label_counter}"
                known_faces[label] = face_encoding
                face_label_counter += 1

                top, right, bottom, left = face_locations[i]
                face_image = image[top:bottom, left:right]
                pil_image = Image.fromarray(face_image)
                face_path = os.path.join(known_faces_dir, f"{label}.jpg")
                pil_image.save(face_path)
                face_url = f"/known_faces/{label}.jpg"
                face_urls.append(face_url)

    return face_urls

@app.put("/upload")
async def upload_photos(files: List[UploadFile] = File(...)):
    for file in files:
        with open(f"./input_photos/{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    return {"message": "files uploaded successfully"}

@app.get("/detect-faces")
async def detect_faces_endpoint():
    input_dir = "./input_photos"
    known_faces_dir = "./known_faces"
    face_urls = process_input_folder(input_dir, known_faces_dir)
    return {"message": "Faces detected and saved", "face_urls": face_urls}

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    input_dir = "./input_photos"
    known_faces_dir = "./known_faces"
    output_dir = "./output_sorted_photos"

    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(known_faces_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=7000, reload=True)