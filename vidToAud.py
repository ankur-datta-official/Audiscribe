import os
from moviepy import VideoFileClip


def extract_audio(video_path, output_path):
    """Extracts audio from a video file and saves it as a WAV file."""
    try:
        video = VideoFileClip(video_path)
        audio_path = os.path.join(output_path, os.path.basename(video_path).rsplit(".", 1)[0] + ".wav")
        video.audio.write_audiofile(audio_path, codec="pcm_s16le")  # Save as WAV
        return audio_path
    except Exception as e:
        print(f"Error extracting audio: {e}")
        return None



