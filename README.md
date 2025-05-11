# Telegram Reverse Shell Bot

A Python-based remote administration tool using Telegram's Bot API for secure command execution and system control.

## ⚠️ Warning
**This tool provides remote system access.**  
- Use only on systems you own or have explicit permission to control  
- Never expose this on production systems without additional security  
- The creator is not responsible for misuse  

## 📋 Features
- Execute remote system commands via Telegram
- Two-way communication (send/receive messages)
- Built-in logging and error reporting
- Cross-platform support (Windows/Linux/macOS)
- Custom commands (`/send`, `exit`)

## 🛠️ Setup Guide

### 1. Create a Telegram Bot
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` and follow prompts
3. Copy your bot token (will look like `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

### 2. Get Your Chat ID
#### Method A: Using ID Bot
1. Search for `@userinfobot` in Telegram
2. Start a chat and send `/start`
3. Note your numerical `Id`

#### Method B: Manual Discovery
```python
import requests
BOT_TOKEN = "YOUR_BOT_TOKEN"
updates = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates").json()
print(updates)  # Send a message to your bot first

#### DEV BY @RITH
