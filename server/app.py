from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS
from Chatbot import  generate_response
import nltk

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger_eng')

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Hello, There!"
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
        print(f"Error:{e}")
        return jsonify({'error': 'Internal server error','message': str(e)}), 500
    
def api():
    try:
        user_input = request.get_json()['message']
        response = generate_response(user_input)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})
    
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)

