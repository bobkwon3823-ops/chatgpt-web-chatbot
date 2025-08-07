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
            "model": "mistralai/mixtral-8x7b",
            "messages": [
                {"role": "user", "content": user_input}
            ]
        }

        response = requests.post(API_URL, headers=headers, json=data)
        print("📡 응답 상태코드:", response.status_code)
        print("📡 응답 내용:", response.text)

        response_data = response.json()
        reply = response_data["choices"][0]["message"]["content"]

    except Exception as e:
        print("❌ 예외 발생:", str(e))
        return jsonify({"reply": f"❌ 오류가 발생했습니다: {str(e)}"})

    return jsonify({"reply": reply})