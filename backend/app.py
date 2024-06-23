# 상세 정보
# 라우트 /upload: 파일 업로드, 번역, 번역된 파일 다운로드, 텍스트 추출 수행
# 라우트 /delete: 업로드된 파일 삭제
# 라우트 /json: JSON 데이터 반환
# 라우트 /html: HTML 페이지 반환
# 라우트 /upload-form: 파일 업로드 용 폼

import os
import requests
import uuid
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from flask import Flask, request, jsonify, render_template_string
from urllib import parse, error
import base64
import json
import sys

app = Flask(__name__)

# Directory to save uploaded files
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Papago API configuration
PAPAGO_API_URL = "https://naveropenapi.apigw.ntruss.com/doc-trans/v1"
API_KEY_ID = "h9r6m27w0d"
API_KEY = "7PbdD8RtQR0AyEwsp11tvqjazukN33AfAePbhuAa"
TARGET_LANG = 'ko'  # Target language for translation

# Epson API configuration
EPSON_HOST = 'api.epsonconnect.com'
EPSON_CLIENT_ID = 'bbea82536e774efa93eb2ce1fb769f4a'
EPSON_SECRET = 'Q74Edy4fCUcU7xSUoFKyT4flZCq2Tgosxr7q2OJI6wkuSwk0ALtzsfaTXFZQSmMm'
EPSON_DEVICE = 'masterofapi@print.epsonconnect.com'

# Route to handle file uploads and translation
@app.route('/upload', methods=['GET', 'POST'])
def upload_and_translate_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Call Papago API for document translation
        try:
            request_id = translate_document(file_path)
            if not request_id:
                return jsonify({'error': 'Translation request failed'}), 500

            # Download the translated document
            translated_file_path = os.path.join(UPLOAD_FOLDER, f'translated_{file.filename}')
            download_translated_document(request_id, translated_file_path)

            # Extract text from the translated document using OCR
            extracted_text = extract_text_from_pdf_with_ocr(translated_file_path)

            return render_template_string(upload_success_html, filename=file.filename, extracted_text=extracted_text)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        files = os.listdir(UPLOAD_FOLDER)
        return render_template_string(upload_form_html, files=files)

# Route to handle printing the extracted text
@app.route('/print', methods=['POST'])
def print_extracted_text():
    extracted_text = request.form.get('extracted_text')
    if not extracted_text:
        return jsonify({'error': 'No text to print'}), 400

    try:
        auth_response = authenticate()
        if not auth_response:
            return jsonify({'error': 'Authentication failed'}), 500

        subject_id = auth_response.get('subject_id')
        access_token = auth_response.get('access_token')

        # Create a print job
        job_response = create_print_job(access_token, subject_id)
        if not job_response:
            return jsonify({'error': 'Failed to create print job'}), 500

        job_id = job_response.get('id')
        base_uri = job_response.get('upload_uri')

        # Upload the text as a print file
        text_file_path = os.path.join(UPLOAD_FOLDER, 'extracted_text.txt')
        with open(text_file_path, 'w', encoding='utf-8') as f:
            f.write(extracted_text)

        upload_response = upload_print_file(base_uri, text_file_path)
        if not upload_response:
            return jsonify({'error': 'Failed to upload print file'}), 500

        # Execute the print job
        print_response = execute_print(access_token, subject_id, job_id)
        if not print_response:
            return jsonify({'error': 'Failed to execute print job'}), 500

        return jsonify({'message': 'Text printed successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Function to call Papago API for document translation
def translate_document(file_path):
    with open(file_path, 'rb') as file:
        data = {
            'source': 'en',  # Source language
            'target': TARGET_LANG,
            'file': (file_path, file, 'application/octet-stream', {'Content-Transfer-Encoding': 'binary'})
        }
        m = MultipartEncoder(data, boundary=uuid.uuid4())
        headers = {
            "Content-Type": m.content_type,
            "X-NCP-APIGW-API-KEY-ID": API_KEY_ID,
            "X-NCP-APIGW-API-KEY": API_KEY
        }
        response = requests.post(f"{PAPAGO_API_URL}/translate", headers=headers, data=m.to_string())

        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('requestId')
        else:
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

# Function to download the translated document
def download_translated_document(request_id, output_file_path):
    download_url = f"{PAPAGO_API_URL}/download?requestId={request_id}"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": API_KEY_ID,
        "X-NCP-APIGW-API-KEY": API_KEY
    }
    response = requests.get(download_url, headers=headers)

    if response.status_code == 200:
        with open(output_file_path, 'wb') as f:
            f.write(response.content)
    else:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

# Function to extract text from PDF using OCR
def extract_text_from_pdf_with_ocr(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img, lang='kor')  # Set language to Korean
    return text

# Epson API functions
def authenticate():
    AUTH_URI = f'https://{EPSON_HOST}/api/1/printing/oauth2/auth/token?subject=printer'
    auth = base64.b64encode(f"{EPSON_CLIENT_ID}:{EPSON_SECRET}".encode()).decode()
    query_param = {
        'grant_type': 'password',
        'username': EPSON_DEVICE,
        'password': ''
    }
    query_string = parse.urlencode(query_param)
    headers = {
        'Authorization': f'Basic {auth}',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'
    }

    try:
        req = requests.post(AUTH_URI, data=query_string, headers=headers)
        if req.status_code == HTTPStatus.OK:
            return req.json()
        else:
            print(f"Failed to authenticate: {req.status_code} - {req.reason}")
            return None
    except requests.RequestException as e:
        print(f"Request exception: {e}")
        return None

def create_print_job(access_token, subject_id):
    job_uri = f'https://{EPSON_HOST}/api/1/printing/printers/{subject_id}/jobs'
    data_param = {
        'job_name': 'SampleJob1',
        'print_mode': 'document'
    }
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json;charset=utf-8'
    }

    try:
        req = requests.post(job_uri, json=data_param, headers=headers)
        if req.status_code == HTTPStatus.CREATED:
            return req.json()
        else:
            print(f"Failed to create print job: {req.status_code} - {req.reason}")
            return None
    except requests.RequestException as e:
        print(f"Request exception: {e}")
        return None

def upload_print_file(base_uri, file_path):
    upload_uri = f"{base_uri}&File={os.path.basename(file_path)}"
    headers = {
        'Content-Length': str(os.path.getsize(file_path)),
        'Content-Type': 'application/octet-stream'
    }

    try:
        with open(file_path, 'rb') as f:
            req = requests.post(upload_uri, data=f, headers=headers)
            if req.status_code == HTTPStatus.OK:
                return req.json()
            else:
                print(f"Failed to upload print file: {req.status_code} - {req.reason}")
                return None
    except requests.RequestException as e:
        print(f"Request exception: {e}")
        return None

def execute_print(access_token, subject_id, job_id):
    print_uri = f'https://{EPSON_HOST}/api/1/printing/printers/{subject_id}/jobs/{job_id}/print'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json; charset=utf-8'
    }

    try:
        req = requests.post(print_uri, headers=headers)
        if req.status_code == HTTPStatus.OK:
            return req.json()
        else:
            print(f"Failed to execute print job: {req.status_code} - {req.reason}")
            return None
    except requests.RequestException as e:
        print(f"Request exception: {e}")
        return None

# Route to handle file deletion
@app.route('/delete', methods=['POST'])
def delete_file():
    filename = request.form['filename']
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return render_template_string(file_deleted_html, filename=filename), 200
    else:
        return jsonify({'error': 'File not found'}), 404

# HTML templates
upload_form_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Upload and Translation</title>
</head>
<body>
    <h1>Upload and Translate a File</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
    <h2>Uploaded Files</h2>
    <ul>
        {% for filename in files %}
        <li>
            {{ filename }}
            <form action="/delete" method="post" style="display:inline;">
                <input type="hidden" name="filename" value="{{ filename }}">
                <input type="submit" value="Delete">
            </form>
        </li>
        {% endfor %}
    </ul>
</body>
</html>
"""

upload_success_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Uploaded</title>
</head>
<body>
    <h1>File {{ filename }} uploaded and translated successfully</h1>
    <h2>Extracted Text:</h2>
    <pre>{{ extracted_text }}</pre>
    <form action="/print" method="post">
        <input type="hidden" name="extracted_text" value="{{ extracted_text }}">
        <input type="submit" value="Print">
    </form>
    <form action="/upload" method="get">
        <input type="submit" value="Go Back">
    </form>
</body>
</html>
"""

file_deleted_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Deleted</title>
</head>
<body>
    <h1>File {{ filename }} deleted successfully</h1>
    <form action="/upload" method="get">
        <input type="submit" value="Go Back">
    </form>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)
