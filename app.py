import os
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import cv2
import pytesseract
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SEGMENT_FOLDER'] = 'static/segments'

# Azure Computer Vision credentials
subscription_key = "AZURE_SUBSCRIPTION_KEY"
endpoint = "AZURE_ENDPOINT"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['SEGMENT_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return redirect(request.url)

    file = request.files['image']
    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = secure_filename(file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(image_path)

        # Clear previous segments
        clear_segments()

        text = extract_text(image_path)
        segments = segment_image(image_path)

        return render_template('result.html', text=text, segments=segments)

def clear_segments():
    segment_folder = app.config['SEGMENT_FOLDER']
    for filename in os.listdir(segment_folder):
        file_path = os.path.join(segment_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

def extract_text(image_path):
    # Use Azure's OCR
    with open(image_path, "rb") as image_stream:
        ocr_result = computervision_client.read_in_stream(image_stream, raw=True)

    operation_location = ocr_result.headers["Operation-Location"]
    operation_id = operation_location.split("/")[-1]

    while True:
        result = computervision_client.get_read_result(operation_id)
        if result.status not in ['notStarted', 'running']:
            break

    if result.status == 'succeeded':
        text = "\n".join([line.text for read_result in result.analyze_result.read_results for line in read_result.lines])
        return text
    else:
        return "No text found."

def segment_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    segments = []

    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        if w > 50 and h > 50:  # Filter out small segments
            segment = image[y:y+h, x:x+w]
            segment_filename = f"{os.path.basename(image_path).split('.')[0]}_segment_{i}.png"
            segment_path = os.path.join(app.config['SEGMENT_FOLDER'], segment_filename)
            cv2.imwrite(segment_path, segment)
            segments.append(f"segments/{segment_filename}")

    return segments

if __name__ == '__main__':
    app.run(debug=True)
