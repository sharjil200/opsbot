import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
VERSION = os.getenv("APP_VERSION", "1.0.0")

@app.route("/")
def index():
    return render_template("index.html", version=VERSION)

@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="healthy", service="opsbot", version=VERSION), 200

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    user_query = data.get("query", "").lower()

    if "status" in user_query or "health" in user_query:
        reply = "🔍 **SRE Diagnostic:** All core subsystems are operational. No active memory or CPU bottlenecks detected on the node."
    elif "metrics" in user_query or "traffic" in user_query:
        reply = "📊 **Telemetry Data:** HTTP request rate is stable at 0.4 req/sec. Average response latency: `12ms`."
    elif "hello" in user_query or "hi" in user_query:
        reply = "👋 Hello, Engineer! I am **OpsBot**, your autonomous SRE assistant. Ask me about system health, metrics, or incident runbooks."
    else:
        reply = f"🤖 **OpsBot AI:** I processed your query: *'{user_query}'*. System is nominal. Try asking about **'system status'** or **'metrics'**."

    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
