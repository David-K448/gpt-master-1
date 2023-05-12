from flask import Flask, render_template, request, session, redirect, url_for, flash, send_from_directory
import os
import tempfile
import atexit
import shutil
import time
import openai
from google.cloud import translate_v2 as translate
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'tmp'
last_click_time = 0

api_key = os.getenv('OPENAI_KEY')
openai.api_key = api_key
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:\Users\killi\OneDrive\Desktop\stuffgpt\translation-stuff-386514-c6a00efd32ba.json"
fileNameA = ''

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    MAX_FILESIZE = 25 * 1024 * 1024 # 25MB in bytes
    if file.content_length > MAX_FILESIZE:
        flash("File is too large. Max file size is 25MB.")
        return redirect('/')
    file.save(os.path.join(os.getcwd(), 'tmp', file.filename))
    return render_template('uploaded.html', file=file)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    global fileNameA
    fileNameA = filename 
    print(fileNameA)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)




@app.route('/scribe_btn_click', methods=['POST'])
def button_click():
    global last_click_time, fileNameA
    now = time.time()
    if now - last_click_time < 1:
        # Ignore the button click if it is clicked too quickly
        return '', 204
    else:
        last_click_time = now
        # Handle the button click
        op_api()
        return 'Button clicked successfully!', 200
    
def op_api():
    with open(os.path.join(app.config['UPLOAD_FOLDER'], fileNameA), 'rb') as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        transcription_text = transcript.text
        print(transcription_text)


if __name__ == '__main__':
    app.run()
