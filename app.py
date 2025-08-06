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
    user_input = request.json["message"]
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/mixtral-8x7b",  # 무료 모델로 시도
        "messages": [
            {"role": "user", "content": user_input}
        ]
    }

    response = requests.post(API_URL, headers=headers, json=data)

    # 🔽 응답 확인용 로그
    print("📡 응답 상태코드:", response.status_code)
    print("📡 응답 내용:", response.text)

    try:
        response_data = response.json()
        reply = response_data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, ValueError) as e:
        reply = f"❌ API 응답 오류가 발생했습니다: {e}"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
