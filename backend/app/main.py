# app/main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import shutil
import os
import uuid

from .utils.ppt_convertor import convert_pptx_to_images
from .utils.ppt_parser import extract_ppt_content
from .utils.audio_generator import generate_audio_files
from .utils.video_creator import create_video_from_images_and_audio


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload/")
async def upload_ppt(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    ppt_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.pptx")

    with open(ppt_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    slides_content = extract_ppt_content(ppt_path)
    audio_files = generate_audio_files(slides_content, file_id)
    slide_image_files = convert_pptx_to_images(ppt_path, file_id)
    video_path = create_video_from_images_and_audio(slide_image_files, audio_files, file_id)

    return FileResponse(video_path, media_type="video/mp4", filename="lecture.mp4")

