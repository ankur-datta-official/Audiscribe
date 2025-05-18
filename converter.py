import os
import speech_recognition as sr
from pydub import AudioSegment

def convert_to_wav(filepath):
    """
    Convert audio file to WAV format if it's not already in WAV format.
    
    Args:
    - filepath (str): Path of the uploaded audio file.

    Returns:
    - str: Path to the WAV file.
    """
    # Get the file extension
    ext = os.path.splitext(filepath)[1].lower()

    # If the file is already in WAV format, return it
    if ext == '.wav':
        return filepath

    # Convert to WAV
    audio = AudioSegment.from_file(filepath)
    
    # Create WAV filename
    wav_filepath = filepath.rsplit('.', 1)[0] + '.wav'
    
    # Export as WAV
    audio.export(wav_filepath, format='wav')
    
    return wav_filepath

def process_audio(filepath, output_folder):
    # Convert to WAV format if needed
    wav_filepath = convert_to_wav(filepath)

    recognizer = sr.Recognizer()

    # Read and process the audio file
    with sr.AudioFile(wav_filepath) as source:
        audio = recognizer.record(source)

    # Initialize transcript
    transcript = ""

    try:
        transcript = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        transcript = "Could not understand the audio."
    except sr.RequestError:
        transcript = "Error with the Google API."

    # Save transcript as .txt file
    text_filename = f"{os.path.splitext(os.path.basename(filepath))[0]}.txt"
    output_path = os.path.join(output_folder, text_filename)

    with open(output_path, "w") as text_file:
        text_file.write(transcript)

    # Clean up: remove the converted WAV file if it was created
    if wav_filepath != filepath:
        os.remove(wav_filepath)

    return transcript, text_filename
