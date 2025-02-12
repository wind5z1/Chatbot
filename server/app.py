from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, There!"
@app.route('/api', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get['message', '']
    response_text = f'You said: {message}'
    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(debug=True)
