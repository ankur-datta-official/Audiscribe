from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, send_file
import os
import cv2
from converter import process_audio  # Import conversion logic
from vidToAud import extract_audio

# Initialize Flask app
app = Flask(__name__)

# Folder configuration
UPLOAD_FOLDER = 'static/uploads'
OUTPUT_FOLDER = 'static/output'
EXTRACTED_AUDIO_FOLDER = "static/audio"
PROCESSED_TEXT_FOLDER = "static/output"
ALLOWED_EXTENSIONS = {"mp4", "avi", "mov", "mkv"}

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(EXTRACTED_AUDIO_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_TEXT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Route for homepage
@app.route('/')
def index():
    return render_template('index.html', transcript='', text_filename='')

# Route for homepage
@app.route('/content')
def content():
    return render_template('letsGo.html', transcript='', text_filename='')

# Route for transcribe page
@app.route('/transcribe', methods=['GET', 'POST'])
def transcribe():
    transcript = ""
    text_filename = ""

    if request.method == 'POST':
        if 'audio_file' not in request.files:
            return redirect(request.url)

        file = request.files['audio_file']

        if file.filename == '':
            return redirect(request.url)

        # Save the uploaded audio file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Process audio and get the transcript
        transcript, text_filename = process_audio(filepath, app.config['OUTPUT_FOLDER'])

    return render_template('transcribe.html', transcript=transcript, text_filename=text_filename)

# Route to download the text file
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload_video", methods=["GET", "POST"])
def upload_video():
    """Handles video file upload and extraction process."""
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file selected", "error")
            return redirect(request.url)

        file = request.files["file"]

        if file.filename == "":
            flash("No selected file", "error")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            video_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(video_path)

            # Extract audio
            audio_path = extract_audio(video_path, EXTRACTED_AUDIO_FOLDER)
            if audio_path:
                return redirect(url_for("convert_audio", filename=os.path.basename(audio_path)))

    return render_template("upload_video.html")


@app.route("/convert/<filename>")
def convert_audio(filename):
    """Redirects the extracted audio to converter.py for text conversion."""
    audio_path = os.path.join(EXTRACTED_AUDIO_FOLDER, filename)
    if os.path.exists(audio_path):
        return redirect(url_for("transcribe", filename=filename))  # Redirect to transcribe function in converter.py
    else:
        flash("Audio extraction failed.", "error")
        return redirect(url_for("upload_video"))
    

@app.route('/technologies')
def technologies():
    return render_template('technologies.html')

@app.route('/documentation')
def documentation():
    return render_template('documentation.html')



if __name__ == '__main__':
    app.run(debug=True)
