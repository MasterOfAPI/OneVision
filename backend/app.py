# 라우트 /upload: 파일 업로드, 번역, 번역된 파일 다운로드, 텍스트 추출 수행
# 라우트 /delete: 업로드된 파일 삭제
# 라우트 /json: JSON 데이터 반환
# 라우트 /html: HTML 페이지 반환
# 라우트 /upload-form: 파일 업로드 용 폼

from flask import Flask, request, jsonify, render_template_string, redirect, url_for
import os
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import uuid
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

app = Flask(__name__)

# Directory to save uploaded and translated files
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Naver Papago API configuration
API_URL = "https://naveropenapi.apigw.ntruss.com/doc-trans/v1"
API_KEY_ID = "h9r6m27w0d"
API_KEY = "7PbdD8RtQR0AyEwsp11tvqjazukN33AfAePbhuAa"

def translate_document(file_path, source_lang='en', target_lang='ko'):
    with open(file_path, 'rb') as file:
        data = {
            'source': source_lang,
            'target': target_lang,
            'file': (file_path, file, 'application/octet-stream', {'Content-Transfer-Encoding': 'binary'})
        }
        m = MultipartEncoder(data, boundary=uuid.uuid4())

        headers = {
            "Content-Type": m.content_type,
            "X-NCP-APIGW-API-KEY-ID": API_KEY_ID,
            "X-NCP-APIGW-API-KEY": API_KEY
        }

        response = requests.post(f"{API_URL}/translate", headers=headers, data=m.to_string())

        if response.status_code == 200:
            return response.json()['requestId']
        else:
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

def download_translated_document(request_id, output_file_path):
    download_url = f"{API_URL}/download?requestId={request_id}"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": API_KEY_ID,
        "X-NCP-APIGW-API-KEY": API_KEY
    }
    response = requests.get(download_url, headers=headers)

    if response.status_code == 200:
        with open(output_file_path, 'wb') as f:
            f.write(response.content)
        return output_file_path
    else:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

def extract_text_from_pdf_with_ocr(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for i, img in enumerate(images):
        text += pytesseract.image_to_string(img, lang='kor')
    return text

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    # Translate the uploaded file
    try:
        request_id = translate_document(file_path)
        translated_file_path = download_translated_document(request_id, file_path.replace('.pdf', '_translated.pdf'))
        extracted_text = extract_text_from_pdf_with_ocr(translated_file_path)
        return jsonify({'message': f'File {file.filename} uploaded, translated, and text extracted successfully', 'extracted_text': extracted_text}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete', methods=['POST'])
def delete_file():
    filename = request.form['filename']
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({'message': f'File {filename} deleted successfully'}), 200
    else:
        return jsonify({'error': 'File not found'}), 404

@app.route('/json', methods=['GET'])
def return_json():
    data = {
        'key1': 'value1',
        'key2': 'value2',
    }
    return jsonify(data)

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

@app.route('/upload-form', methods=['GET'])
def upload_form():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>File Upload</title>
    </head>
    <body>
        <h1>Upload a File</h1>
        <form id="uploadForm" action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <button type="button" onclick="uploadFile()">Upload</button>
        </form>
        <h2>Uploaded Files</h2>
        <ul id="fileList"></ul>
        <script>
            async function uploadFile() {
                const form = document.getElementById('uploadForm');
                const formData = new FormData(form);
                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();
                alert(result.message);
                if (result.extracted_text) {
                    const translatedDiv = document.createElement('div');
                    translatedDiv.innerText = 'Extracted Text: ' + result.extracted_text;
                    document.body.appendChild(translatedDiv);
                }
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(debug=True)
