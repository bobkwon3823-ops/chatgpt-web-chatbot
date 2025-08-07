from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json["message"]
        print("📨 사용자 메시지:", user_input)

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "mistralai/mixtral-8x7b",  # 무료/안정적인 모델로 변경
            "messages": [
                {"role": "user", "content": user_input}
            ]
        }

        response = requests.post(API_URL, headers=headers, json=data)
        print("📡 응답 상태코드:", response.status_code)
        print("📡 응답 내용:", response.text)

        response_data = response.json()

        # 여기에 핵심 변경 사항 있음
        if "choices" in response_data:
            reply = response_data["choices"][0]["message"]["content"]
        else:
            # API 응답을 직접 사용자에게 보여줌
            reply = f"❌ API 응답 오류: {response_data}"

    except Exception as e:
        print("❌ 예외 발생:", str(e))
        reply = f"❌ 서버 오류 발생: {str(e)}"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
