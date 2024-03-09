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

if __name__ == '__main__':
    app.run(debug=True)
