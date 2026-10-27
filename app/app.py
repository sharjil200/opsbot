import os
import psutil
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
    
    # Gather real-time EC2 server stats
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    if "status" in user_query or "health" in user_query or "server" in user_query:
        reply = (
            f"🔍 **Live SRE Server Diagnostic:**\n"
            f"- **CPU Usage:** `{cpu_usage}%`\n"
            f"- **Memory Usage:** `{memory.percent}%` (Used: {round(memory.used / (1024**3), 2)} GB / Total: {round(memory.total / (1024**3), 2)} GB)\n"
            f"- **Disk Usage:** `{disk.percent}%`\n"
            f"- **Status:** All core subsystems operational and stable."
        )
    elif "metrics" in user_query or "traffic" in user_query or "cpu" in user_query:
        reply = (
            f"📊 **Real-Time Telemetry Data:**\n"
            f"```text\n"
            f"CPU Load: {cpu_usage}%\n"
            f"RAM Free: {round(memory.available / (1024**3), 2)} GB\n"
            f"Disk Free: {round(disk.free / (1024**3), 2)} GB\n"
            f"```"
        )
    elif "hello" in user_query or "hi" in user_query:
        reply = "👋 Hello, Engineer! I am **OpsBot**, your autonomous SRE assistant. I am actively monitoring this AWS EC2 instance. Ask me about **'system status'** or **'metrics'**."
    else:
        reply = f"🤖 **OpsBot AI:** I processed your query: *'{user_query}'*. Server load is nominal (CPU: {cpu_usage}%). Try asking about **'system status'** or **'metrics'**."

    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
