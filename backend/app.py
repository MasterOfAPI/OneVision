# 상세 정보
# 라우트 /upload: 파일 업로드, 번역, 번역된 파일 다운로드, 텍스트 추출 수행
# 라우트 /delete: 업로드된 파일 삭제
# 라우트 /json: JSON 데이터 반환
# 라우트 /html: HTML 페이지 반환
# 라우트 /upload-form: 파일 업로드 용 폼

# Test 방법
# curl -X POST http://127.0.0.1:5000/upload -F "file=@/path/to/your/file.pdf" << 파일 업로드
# curl -X POST http://127.0.0.1:5000/delete -d "filename=file.pdf" << 파일 삭제
# curl http://127.0.0.1:5000/json << JSON 응답 테스트
# curl http://127.0.0.1:5000/html << HTML 응답 테스트

import os
import requests
import uuid
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from flask import Flask, request, jsonify, render_template_string
from requests_toolbelt.multipart.encoder import MultipartEncoder

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

            return jsonify({
                'message': f'File {file.filename} uploaded and translated successfully',
                'extracted_text': extracted_text
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        # Render the upload form
        html_content = """
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
        files = os.listdir(UPLOAD_FOLDER)
        return render_template_string(html_content, files=files)

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
    for i, img in enumerate(images):
        text += pytesseract.image_to_string(img, lang='kor')  # Set language to Korean
    return text

# Route to handle file deletion
@app.route('/delete', methods=['POST'])
def delete_file():
    filename = request.form['filename']
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return render_template_string("""
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
        """, filename=filename), 200
    else:
        return jsonify({'error': 'File not found'}), 404

# Route to return JSON response
@app.route('/json', methods=['GET'])
def return_json():
    data = {
        'key1': 'value1',
        'key2': 'value2',
    }
    return jsonify(data)

# Route to return HTML response
@app.route('/html', methods=['GET'])
def return_html():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>HTML Response</title>
    </head>
    <body>
        <h1>Hello, this is an HTML response!</h1>
    </body>
    </html>
    """
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(debug=True)
