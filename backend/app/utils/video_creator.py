from moviepy.video.VideoClip import ImageClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy import concatenate_videoclips
import os

def create_video_from_images_and_audio(slide_image_paths, audio_paths, file_id, upload_folder="uploads"):
    if len(slide_image_paths) != len(audio_paths):
        raise ValueError("Number of slide images and audio files must match.")

    clips = []
    audio_clips_to_close = []

    try:
        for i in range(len(slide_image_paths)):
            image_path = slide_image_paths[i]
            audio_path = audio_paths[i]

            audio_clip = AudioFileClip(audio_path)
            audio_clips_to_close.append(audio_clip)
            duration = audio_clip.duration

            image_clip = ImageClip(image_path).with_duration(duration).with_audio(audio_clip)
            clips.append(image_clip)

        final_video = concatenate_videoclips(clips, method="compose")
        output_path = os.path.abspath(os.path.join(upload_folder, file_id, "final_lecture.mp4"))
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")

        # Close video clip to release handles
        final_video.close()
        for clip in clips:
            clip.close()

        return output_path
    finally:
        for ac in audio_clips_to_close:
            try:
                ac.close()
            except Exception:
                pass