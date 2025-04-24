# app/utils/video_creator.py
from moviepy.video.VideoClip import ImageClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy import concatenate_videoclips
import os

def create_video_from_images_and_audio(slide_image_paths, audio_paths, file_id):
    if len(slide_image_paths) != len(audio_paths):
        raise ValueError("Number of slide images and audio files must match.")

    clips = []

    for i in range(len(slide_image_paths)):
        image_path = slide_image_paths[i]
        audio_path = audio_paths[i]

        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration

        image_clip = ImageClip(image_path).with_duration(duration).with_audio(audio_clip)
        clips.append(image_clip)

    final_video = concatenate_videoclips(clips, method="compose")
    output_path = f"uploads/{file_id}/final_lecture.mp4"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    final_video.write_videofile(output_path, fps=24)

    return output_path
