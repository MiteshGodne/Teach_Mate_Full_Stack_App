from gtts import gTTS
import os

def generate_audio_files(slides, file_id, upload_folder="uploads"):
    folder = os.path.join(upload_folder, file_id, "audio")
    os.makedirs(folder, exist_ok=True)
    audio_paths = []

    for i, slide in enumerate(slides):
        text = slide.get("text", "").strip()
        if not text:
            text = " "
        tts = gTTS(text=text, lang='en')
        audio_path = os.path.join(folder, f"slide_{i+1}.mp3")
        tts.save(audio_path)
        audio_paths.append(audio_path)

    return audio_paths