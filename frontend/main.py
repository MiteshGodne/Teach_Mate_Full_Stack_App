from fastapi import FastAPI, UploadFile, File

app = FastAPI()
@app.get("/g/")
async def backend_screen():
    return "Welcome To The backend of TeachMate !!"
