from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    print("✅ [서버 진입] /chat 요청 받음")

    try:
        user_input = request.json["message"]
        print("📨 사용자 메시지:", user_input)

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "mistralai/mixtral-8x7b",  # 안정적인 무료 모델
            "messages": [
                {"role": "user", "content": user_input}
            ]
        }

        response = requests.post(API_URL, headers=headers, json=data)
        print("📡 응답 상태코드:", response.status_code)
        print("📡 응답 내용:", response.text)

        response_data = response.json()

        # 예외 없이 진행됐을 때만 'choices' 접근
        if "choices" in response_data:
            reply = response_data["choices"][0]["message"]["content"]
        else:
            reply = f"❌ API 응답 오류: {response_data}"

    except Exception as e:
        print("❌ 예외 발생:", str(e))
        reply = f"❌ 서버 오류 발생: {str(e)}"

    return jsonify({"reply": reply})
