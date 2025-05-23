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

# Allow GET and HEAD to suppress 405 logs from health checks
@app.api_route("/", methods=["GET", "HEAD"])
async def root():
    return {"message": "Welcome, This is Teach Mate"}

# CORS: only the domain, not the full path
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://teach-mate-full-stack-app.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.options("/upload/")
async def options_upload():
    return {"message": "Options request handled"}

# Use /tmp for safe file writing in Render
UPLOAD_FOLDER = "/tmp/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload")
@app.post("/upload/")
async def upload_ppt(file: UploadFile = File(...)):
    try:
        file_id = str(uuid.uuid4())
        ppt_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.pptx")

        # Save uploaded PPT file
        with open(ppt_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Process: extract content, generate audio, convert slides, create video
        slides_content = extract_ppt_content(ppt_path)
        audio_files = generate_audio_files(slides_content, file_id)
        slide_image_files = convert_pptx_to_images(ppt_path, file_id)
        video_path = create_video_from_images_and_audio(slide_image_files, audio_files, file_id)

        return FileResponse(video_path, media_type="video/mp4", filename="lecture.mp4")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")



# # app/main.py
# from fastapi import FastAPI, UploadFile, File
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import FileResponse
# import shutil
# import os
# import uuid

# from app.utils.ppt_convertor import convert_pptx_to_images
# from app.utils.ppt_parser import extract_ppt_content
# from app.utils.audio_generator import generate_audio_files
# from app.utils.video_creator import create_video_from_images_and_audio


# app = FastAPI()

# @app.get("/")
# async def root():
#     return {"message": "Welcome, This is Teach Mate"}

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["https://teach-mate-full-stack-app.vercel.app"],  # React frontend
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# UPLOAD_FOLDER = "tmp/uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.post("/upload")
# @app.post("/upload/")
# async def upload_ppt(file: UploadFile = File(...)):
#     try:
#         file_id = str(uuid.uuid4())
#         ppt_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.pptx")

#         with open(ppt_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         slides_content = extract_ppt_content(ppt_path)
#         audio_files = generate_audio_files(slides_content, file_id)
#         slide_image_files = convert_pptx_to_images(ppt_path, file_id)
#         video_path = create_video_from_images_and_audio(slide_image_files, audio_files, file_id)

#         return FileResponse(video_path, media_type="video/mp4", filename="lecture.mp4")

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

