from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from beignParsing import parse_resume

# Create the Flask app
app = Flask(__name__)

# Enable CORS for all domains on all routes
CORS(app)

@app.route('/api/hello')
def hello_world():
    return jsonify({'message': 'Hello, from Flask!'})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file= request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file and file.filename.endswith('.docx'):
        year = request.form.get('year','2023')
        filename=secure_filename(file.filename)
        filepath=os.path.join('./temp/', filename)
        file.save(filepath)
        combined_data=parse_resume(filepath,year)
        return jsonify(combined_data)

@app.route('/uploadMany', methods=['POST'])
def upload_many_files():
    files = request.files.getlist('files')  # Note the use of getlist here

    if not files:
        return 'No files provided', 400
    responses = []  # To store the response data for each file

    for file in files:
        if file.filename == '':
            # You might want to handle this differently, e.g., by continuing to the next file
            responses.append({'error': 'No selected file'})
            continue

        if file and file.filename.endswith('.docx'):
            year = request.form.get('year', '2023')
            filename = secure_filename(file.filename)
            filepath = os.path.join('./temp/', filename)
            file.save(filepath)
            combined_data = parse_resume(filepath, year)  # Assuming parse_resume returns a dictionary
            responses.append(combined_data)
        else:
            responses.append({'error': 'Invalid file type'})

    return jsonify(responses)

# @app.route('/createExcel', method=['POST'])
# def create_excel():


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
 