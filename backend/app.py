from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

# Directory to save uploaded files
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Route to handle file uploads
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        return render_template_string("""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Upload Complete</title>
                <script type="text/javascript">
                    function goBack() {
                        window.location.href = "/upload";
                    }
                </script>
            </head>
            <body>
                <h1>File {{ filename }} uploaded successfully</h1>
                <button onclick="goBack()">Complete</button>
            </body>
            </html>
        """, filename=file.filename)
    else:
        # Render the upload form
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
                <title>Delete Complete</title>
                <script type="text/javascript">
                    function goBack() {
                        window.location.href = "/upload";
                    }
                </script>
            </head>
            <body>
                <h1>File {{ filename }} deleted successfully</h1>
                <button onclick="goBack()">Complete</button>
            </body>
            </html>
        """, filename=filename)
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
