from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
from Chatbot import generate_response
import nltk
import os
import requests

# 確保 NLTK 需要的資源下載
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
API_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/distilgpt2"
HEADERS={
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}
# Flask 設定
app = Flask(__name__, static_folder='../client', template_folder='../client')
CORS(app)

# 環境變數設定 PORT，確保 Render/Heroku 也能用
port = int(os.environ.get('PORT', 5000))

# 測試路由
@app.route('/')
def home():
    return render_template('index.html')

# API 路由
@app.route('/api', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Invalid request'}), 400

        message = data.get('message', '')
        response_text = generate_response(message)
        return jsonify({'response': response_text})
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

# 靜態文件（例如 script.js, CSS）
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(os.path.join(app.root_path, '../client/static'), filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
