from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import shutil
import os
import uuid

from app.utils.ppt_convertor import convert_pptx_to_images
from app.utils.ppt_parser import extract_ppt_content
from app.utils.audio_generator import generate_audio_files
from app.utils.video_creator import create_video_from_images_and_audio

app = FastAPI()

@app.api_route("/", methods=["GET", "HEAD"])
async def root():
    return {"message": "Welcome, This is Teach Mate"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "https://teach-mate-full-stack-app.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.options("/upload/")
async def options_upload():
    return {"message": "Options request handled"}

# Use environment variable or local current working directory for robustness on Windows/Linux
UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", os.path.join(os.getcwd(), "uploads"))
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload")
@app.post("/upload/")
async def upload_ppt(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    session_folder = os.path.join(UPLOAD_FOLDER, file_id)
    os.makedirs(session_folder, exist_ok=True)
    
    ppt_path = os.path.join(session_folder, f"{file_id}.pptx")

    try:
        # Save uploaded PPT file
        with open(ppt_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Process pipeline with synchronized paths
        slides_content = extract_ppt_content(ppt_path)
        audio_files = generate_audio_files(slides_content, file_id, UPLOAD_FOLDER)
        slide_image_files = convert_pptx_to_images(ppt_path, file_id, UPLOAD_FOLDER)
        video_path = create_video_from_images_and_audio(slide_image_files, audio_files, file_id, UPLOAD_FOLDER)

        if not os.path.exists(video_path):
            raise HTTPException(status_code=500, detail="Video generation failed to produce output file.")

        return FileResponse(video_path, media_type="video/mp4", filename="lecture.mp4")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")