from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# ✅ 환경변수에서 API 키 불러오기
API_KEY = os.getenv("API_KEY")

# ✅ OpenRouter API 설정
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "mistralai/mixtral-8x7b"  # 또는 "openai/gpt-3.5-turbo"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")

    # ✅ API 키가 없을 경우 에러 메시지
    if not API_KEY:
        return jsonify({"reply": "❌ 오류: API 키가 설정되지 않았습니다."}), 500

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": user_input}
        ]
    }

    try:
        # ✅ API 요청
        response = requests.post(API_URL, headers=headers, json=data)

        # ✅ 디버깅용 로그 출력 (Render 로그에서 확인 가능)
        print("✅ [디버깅] 응답 코드:", response.status_code)
        print("✅ [디버깅] 응답 내용:", response.text)

        if response.status_code != 200:
            return jsonify({"reply": f"❌ API 응답 오류: {response.json()}"})

        response_data = response.json()

        # ✅ 'choices'
