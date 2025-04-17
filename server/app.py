from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
from Chatbot import generate_response
import nltk
import os

# NLTKで必要なリソースをダウンロード
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Flask アプリケーションの初期設定
app = Flask(__name__, static_folder='../client', template_folder='../client')
CORS(app)  # CORS（他のドメインからのアクセスを許可）

# ポートの設定（RenderやHerokuなどのホスティングサービスに対応）
port = int(os.environ.get('PORT', 5000))

# ホームページ（ルート）のルーティング設定
@app.route('/')
def home():
    # index.html を表示（クライアント側のトップページ）
    return render_template('index.html')

# チャットボットのAPIエンドポイント（POSTメソッド）
@app.route('/api', methods=['POST'])
def chat():
    try:
        # フロントエンドから送られてきたJSONデータを取得
        data = request.get_json()

        # メッセージが存在するかチェック
        if not data or 'message' not in data:
            return jsonify({'error': 'Invalid request'}), 400

        # ユーザーからのメッセージを取り出す
        message = data.get('message', '')

        # Chatbot モジュールを使って応答を生成
        response_text = generate_response(message)

        # JSON形式で応答を返す
        return jsonify({'response': response_text})
    
    except Exception as e:
        # エラーが発生した場合、エラーメッセージを返す
        print(f"Error: {e}")
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

# 静的ファイル（JSやCSSなど）を返すエンドポイント
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(os.path.join(app.root_path, '../client/static'), filename)

# アプリケーションの起動設定
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
