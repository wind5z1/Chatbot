from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS
from Chatbot import  generate_response

app = Flask(__name__)
CORS(app, origins="*", methods=['GET', 'POST', 'OPTIONS'])  # 允許所有來源訪問

@app.route('/')
def home():
    return "Hello, There!"

@app.route('/api', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    response_text = generate_response(message)
    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(debug=True)

